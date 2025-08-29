

from domain.models.project_dto import ProjectDTO
from domain.models.user_roles_dto import UserRoleReadDTO

from flask import Blueprint, render_template, request, redirect, url_for, \
    jsonify, flash
from flask_login import login_required, current_user
from flask_principal import Permission, RoleNeed
from dependency_injector.wiring import Provide, inject


from infrastructure.container import Container, ProjectCntrl, \
    UserCntrl, UserRolesCntrl

from infrastructure.context import current_project_id, current_user_id

from utils.exception import *
from utils.oc_logger  import OC_logger

log = OC_logger.oc_log("project_rout")



admin = RoleNeed('admin')
admin_permission = Permission(admin)

author = RoleNeed('manager')
author_permission = Permission(author)

bp = Blueprint('project', __name__)

temp = 'cabinet_client/project/'

@login_required
@admin_permission.require(http_exception=403)
@bp.route('/')
@inject
def index(cntrl: ProjectCntrl = Provide[Container.project_cntrl]):
    items = cntrl.get_all()
    return render_template(f'{temp}list.html', items=items, user=current_user)

@login_required
@admin_permission.require(http_exception=403)
@bp.route('/create', methods=['GET', 'POST'])
@inject
def create(cntrl: ProjectCntrl = Provide[Container.project_cntrl]):
    if request.method == 'POST':
        cntrl.create_item(
            request.form['name']
            )
        return redirect(url_for('project.index'))
    return render_template(f'{temp}create.html', user=current_user) 

@login_required
@admin_permission.require(http_exception=403)
@bp.route('/edit/<int:item_id>', methods=['GET', 'POST'])
@inject
def edit(item_id, cntrl: ProjectCntrl = Provide[Container.project_cntrl]):
    item = cntrl.get_item(item_id)
    if item is None:
        print(f"item: {item}")
        return "Нема" 
    if request.method == 'POST':
        cntrl.update_item(
            ProjectDTO(
                id=item.id, 
                name=request.form['name']
            ))
        return redirect(url_for('project.index'))
    return render_template(f'{temp}edit.html', item=item, user=current_user)

@login_required
@admin_permission.require(http_exception=403)
@bp.route('/delete/<int:item_id>', methods=['POST'])
@inject
def delete(item_id, cntrl: ProjectCntrl = Provide[Container.project_cntrl]):
    cntrl.delete_item(item_id)
    return redirect(url_for('project.index'))


@login_required
@admin_permission.require(http_exception=403)
@bp.route('/add_user/', methods=['POST','GET'])
@inject
def add_user(
                cntrl: ProjectCntrl = Provide[Container.project_cntrl],
                user_roles_cntrl: UserRolesCntrl = Provide[Container.user_roles_cntrl],
                ):
    if request.method == 'POST':
        try:
            resp = user_roles_cntrl.add_user(
                request.form.get('email'),
                request.form.get('role_name')
            )
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
    project = cntrl.get_item(current_project_id.get())
    return render_template(
        f'{temp}add_manager.html', 
        project_name=project.name, user=current_user
        )

@login_required
@admin_permission.require(http_exception=403)
@bp.route('/update_user/', methods=['POST','GET'])
@inject
def update_user(
                cntrl: ProjectCntrl = Provide[Container.project_cntrl],
                user_roles_cntrl: UserRolesCntrl = Provide[Container.user_roles_cntrl],
                ):
    if request.method == 'POST':
        try:
            resp = user_roles_cntrl.add_user(
                request.form.get('email'),
                request.form.get('role_name')
            )
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
    project = user_roles_cntrl.get_item(current_project_id.get())
    return render_template(
        f'{temp}update_user.html', 
        project_name=project.name, user=current_user
        )


@bp.route('/list_select', methods=['POST', 'GET'])
@login_required
@author_permission.require(http_exception=403)
@inject 
def list_select(cntrl: ProjectCntrl = Provide[Container.project_cntrl]):
    items = cntrl.get_items_select()
    if items:
        return jsonify({'results': items})
    else:
        return jsonify({'results': []})
