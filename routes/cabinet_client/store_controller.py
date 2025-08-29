


from utils import OC_logger, OSDEBUG
from repository.store_sqlalchemy import StoreRepositorySQLAlchemy
from a_service.store_service import StoreService


from flask import Blueprint, render_template, request, redirect, url_for, \
    jsonify
from flask_login import login_required, current_user

from flask_principal import Permission, RoleNeed

from dependency_injector.wiring import Provide, inject
from infrastructure.container import Container


logger = OC_logger.oc_log('store_cntrl')

admin = RoleNeed('admin')
admin_permission = Permission(admin)

author = RoleNeed('manager')
author_permission = Permission(author)

bp = Blueprint('store', __name__)


temp = 'cabinet_client/store/'

@login_required
@admin_permission.require(http_exception=403)
@bp.route('/')
@inject
def index(service: StoreService = Provide[Container.store_serv]):
    items = service.list_items()
    return render_template(f'{temp}list.html', items=items, user=current_user)

@login_required
@admin_permission.require(http_exception=403)
@bp.route('/create', methods=['GET', 'POST'])
@inject
def create(service: StoreService = Provide[Container.store_serv]):
    try:
        if request.method == 'POST':
            service.create_item(
                request.form['name'], 
                request.form['api'],
                request.form['token'],
                request.form['token_market'] 
                )
            return redirect(url_for('store.index'))
        return render_template(f'{temp}create.html', user=current_user) 
    except Exception as e:
        logger.debug(f'помилка: {e}')
        logger.exception(f'{e}')
        return redirect(url_for('store.index'))
        

@login_required
@admin_permission.require(http_exception=403)
@bp.route('/edit/<int:item_id>', methods=['GET', 'POST'])
@inject
def edit(item_id, service: StoreService = Provide[Container.store_serv]):
    try:
        item = service.get_item(item_id)
        if request.method == 'POST':
            service.update_item(
                item.id, 
                request.form['name'], 
                request.form['api'],
                request.form['token'],
                request.form['token_market']
                )
            if OSDEBUG: print(f'edit:')
            return redirect(url_for('store.index'))
        return render_template(f'{temp}edit.html', item=item, user=current_user)
    except Exception as e:
        logger.debug(f'помилка: {e}')
        logger.exception(f'{e}')
        return redirect(url_for('store.index'))

@login_required
@admin_permission.require(http_exception=403)
@bp.route('/delete/<int:item_id>', methods=['POST'])
@inject
def delete(item_id, service: StoreService = Provide[Container.store_serv]):
    service.delete_item(item_id)
    return redirect(url_for('store.index'))


@bp.route('/list_select', methods=['POST', 'GET'])
@login_required
@author_permission.require(http_exception=403)
@inject
def list_select(service: StoreService = Provide[Container.store_serv]):
    items = service.get_items_select()
    if items:
        return jsonify({'results': items})
    else:
        return jsonify({'results': []})
