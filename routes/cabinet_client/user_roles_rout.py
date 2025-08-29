

from domain.models.project_dto import ProjectDTO
from domain.models.user_roles_dto import UserRoleReadDTO

from flask import Blueprint, render_template, request, redirect, url_for, \
    jsonify, flash
from flask_login import login_required, current_user
from flask_principal import Permission, RoleNeed
from dependency_injector.wiring import Provide, inject


from infrastructure.container import Container, UserRolesCntrl as Cntrl
      

from infrastructure.context import current_project_id, current_user_id

from utils.exception import *
from utils.oc_logger  import OC_logger

log = OC_logger.oc_log("user_roles_rout")


# manager, admin, author
admin = RoleNeed('admin')
admin_permission = Permission(admin)

author = RoleNeed('manager')
author_permission = Permission(author)

bp = Blueprint('user_roles', __name__)

temp = 'cabinet_client/user_roles/'

@login_required
@admin_permission.require(http_exception=403)
@bp.route('/')
@inject
def index(cntrl: Cntrl = Provide[Container.user_roles_cntrl]):
    items = cntrl.get_all()
    return render_template(f'{temp}list.html', items=items, user=current_user)

@login_required
@admin_permission.require(http_exception=403)
@bp.route('/create', methods=['GET', 'POST'])
@inject
def create(cntrl: Cntrl = Provide[Container.user_roles_cntrl]):
    if request.method == 'POST':
        try:
            resp = None
            if resp:
                flash("Додано в проект", "info")
                return redirect(url_for("project.index"))
        except EmailDoesNotExist as e:
            flash("Нема такого емейлу", "error")
            return  redirect(url_for("project.add_user"))
        except RoleNotExist:
            flash("Нема такої Ролі", "error")
            return  redirect(url_for("project.add_user"))
        except Exception as e:
            log.exception(f"add_user: {e}")
            flash("Не вийшло додати в проект", "error")
            return  redirect(url_for("project.add_user"))
    return render_template(
        f'{temp}create.html', user=current_user
        )

@login_required
@admin_permission.require(http_exception=403)
@bp.route('/edit/<int:item_id>', methods=['GET', 'POST'])
@inject
def edit(item_id=None, cntrl: Cntrl = Provide[Container.user_roles_cntrl]):
    if request.method == 'POST':
        try:
            resp = cntrl.update(
                item_id,
                request.form.get('email'),
                request.form.get('role_name')
            )
            if resp:
                flash("Додано в проект", "info")
                return redirect(url_for("user_roles.index"))
        except EmailDoesNotExist as e:
            flash("Нема такого емейлу", "error")
            return  redirect(url_for("user_roles.edit", item_id=item_id))
        except RoleNotExist:
            flash("Нема такої Ролі", "error")
            return  redirect(url_for("user_roles.edit", item_id=item_id))
        except Exception as e:
            log.exception(f"add_user: {e}")
            flash("Не вийшло додати в проект", "error")
            return  redirect(url_for("user_roles.edit", item_id=item_id))
    item = cntrl.get_item(item_id)
    return render_template(
        f'{temp}edit.html', 
        item=item, user=current_user
        )

@login_required
@admin_permission.require(http_exception=403)
@bp.route('/delete/<int:item_id>', methods=['POST'])
@inject
def delete(item_id, cntrl: Cntrl = Provide[Container.user_roles_cntrl]):
    cntrl.delete_item(item_id)
    return redirect(url_for('project.index'))


@bp.route('/list_select', methods=['POST', 'GET'])
@login_required
@author_permission.require(http_exception=403)
@inject 
def list_select(cntrl: Cntrl = Provide[Container.user_roles_cntrl]):
    items = cntrl.get_items_select()
    if items:
        return jsonify({'results': items})
    else:
        return jsonify({'results': []})
