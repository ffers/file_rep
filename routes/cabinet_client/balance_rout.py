import os

from flask import Blueprint, render_template, request, redirect, url_for, \
    jsonify, session
from utils.format_float import format_float


from flask_login import login_required, current_user

from flask_principal import Permission, RoleNeed

from utils import OC_logger

from domain.models.balance_journal_dto import BalanceJournalDTO


from dependency_injector.wiring import Provide, inject
from infrastructure.container import Container, BalanceCntrl

from infrastructure.context import current_project_id, current_user_id

logger = OC_logger.oc_log('balance_cntrl')

admin = RoleNeed('admin') 
admin_permission = Permission(admin)

author = RoleNeed('manager')
author_permission = Permission(author)

bp = Blueprint('balance', __name__)

temp = 'cabinet_client/balance/'

'''
PATH - balance/
'''

@login_required
@admin_permission.require(http_exception=403)
@bp.route('/')
@inject
def index(cntrl: BalanceCntrl = Provide[Container.balance_cntr]):
    print(f"index: {current_project_id.get()}")
    items = cntrl.list_items()
    return render_template(f'{temp}list.html', items=items, user=current_user)

@login_required
@admin_permission.require(http_exception=403)
@bp.route('/create', methods=['GET', 'POST'])
@inject
def create(cntrl: BalanceCntrl = Provide[Container.balance_cntr]):
    try:
        if request.method == 'POST':
            cntrl.create(
                request.form['balance'],
                request.form['wait'],
                request.form['stock'],
                request.form['inwork']
                )
            return redirect(url_for('balance.index'))
        return render_template(f'{temp}create.html', user=current_user) 
    except Exception as e:
        logger.exception(f'create: {e}')
        return 'Exception'

@login_required
@admin_permission.require(http_exception=403)
@bp.route('/edit/<int:item_id>', methods=['GET', 'POST'])
@inject
def edit(item_id, cntrl: BalanceCntrl = Provide[Container.balance_cntr]):
    item = cntrl.get_item(item_id)
    if request.method == 'POST':
        cntrl.update(
            item_id=item.id, 
            balance=request.form['balance'],
            wait=request.form['wait'],
            stock=request.form['stock'],
            inwork=request.form['inwork']
        )
        return redirect(url_for('balance.index'))
    return render_template(f'{temp}edit.html', item=item, user=current_user)

@login_required
@admin_permission.require(http_exception=403)
@bp.route('/delete/<int:item_id>', methods=['POST'])
@inject
def delete(item_id, cntrl: BalanceCntrl = Provide[Container.balance_cntr]):
    cntrl.delete(item_id)
    return redirect(url_for('balance.index'))


@bp.route('/list_select', methods=['POST', 'GET'])
@login_required
@author_permission.require(http_exception=403)
@inject
def list_select(cntrl: BalanceCntrl = Provide[Container.balance_cntr]):
    items = cntrl.get_items_select()
    if items:
        return jsonify({'results': items})
    else:
        return jsonify({'results': []})


@login_required
@admin_permission.require(http_exception=403)
@bp.route('/income', methods=['POST', 'GET'])
@inject
def move_balance(cntrl: BalanceCntrl = Provide[Container.balance_cntr]):
    try:
        if request.method == 'POST':
            move_dto = BalanceJournalDTO(
                income=format_float(request.form['sum']),
                desription=request.form['description'],
                balance_id=2
            )
            print(move_dto)
            item = cntrl.move_balance(move_dto)
            return render_template(f'{temp}move_balance.html', user=current_user)
        else: 
            return render_template(f'{temp}move_balance.html', user=current_user)

    except Exception as e:
        print(f"move_balance помилка {e}")
        return "Помилка"
    

    '''
    временная функция с конкретним айди проекта
    '''
@login_required
@admin_permission.require(http_exception=403)
@bp.route('/project', methods=['GET'])
@inject
def project(cntrl: BalanceCntrl = Provide[Container.balance_cntr]):
    try:
        item = cntrl.get_by_project_id() 
        return render_template(f'{temp}project.html', item=item, user=current_user)
    except Exception as e:
        print(f"income_balance помилка {e}")
        return "Помилка"
    
@login_required
@admin_permission.require(http_exception=403)
@bp.route('/journal')
@inject
def journal(cntrl: BalanceCntrl = Provide[Container.balance_cntr]):
    items = cntrl.get_journal_all()
    return render_template(f'{temp}balance_journal.html', items=items, user=current_user)
