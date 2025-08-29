import os
from flask import Blueprint, render_template, request, \
        flash, redirect, url_for, jsonify, session
from flask_login import login_required, current_user
from flask_principal import Permission, RoleNeed
from flask_paginate import Pagination
from helperkit.filekit import FileKit
from pytz import timezone, utc
from datetime import datetime
from utils import OC_logger
from collections import Counter
from mapper import OrderFormMapper
from DTO import OrderDTO
from utils import OrderedProductSession

from black import OrderCntrl, DeliveryOrderCntrl, ProductCntrl
from dependency_injector.wiring import inject, Provide
from infrastructure.container import Container



OC_log = OC_logger.oc_log("order")

def format_float(num_str):  
    try:  
        num = float(num_str)   
        # Якщо число - ціле, додаємо ".00"
        if num.is_integer():
            num_dr = f"{int(num)}.00"
            return float(num_dr)
        else:
            return float(num)
    except ValueError:
        return "Неправильний формат числа"

def get_data(data, offset=0, per_page=10):
    return data[offset: offset + per_page]

fl_cl = FileKit()


author_permission = Permission(RoleNeed('manager'))
admin_permission = Permission(RoleNeed('admin'))
bp = Blueprint('Order', __name__, template_folder='templates')


@bp.route('/cabinet/orders', methods=['POST', 'GET'])
@login_required
@author_permission.require(http_exception=403)
@inject
def Order(cntrl: OrderCntrl = Provide[Container.order_cntrl]):
    if request.method == 'POST':
        
        print(">>> Add datebase")
        return redirect('/orders')
    else:
        format = "%H:%M:%S %Z%z %Y-%m-%d"
        kiyv = timezone('Europe/Kiev')
        now_utc = datetime.now(timezone('UTC'))
        print(f"Перевірка UTC {now_utc.strftime(format)}")
        kiev_now = now_utc.astimezone(timezone('Europe/Kiev'))
        # Convert to Asia/Kolkata time zone
        now_asia = now_utc.astimezone(timezone('Asia/Kolkata'))
        # now_kiyv = now_utc.astimezone(timezone(kiev))
        print(f"Перевірка {now_asia.strftime(format)}")
        print(kiev_now.strftime(format))
        tasks_orders = cntrl.load_all_order()
        for order in tasks_orders:
            # установити UTC
            if order.timestamp.tzinfo is None or order.timestamp.tzinfo.utcoffset(order.timestamp) is None:
                order.timestamp = order.timestamp.replace(tzinfo=utc)
            # установити Київ час
            order.timestamp = order.timestamp.astimezone(kiyv)
            # order.sum_price = "{:.2f}".format(order.sum_price)

        page = request.args.get('page', default=1, type=int)
        per_page = 50

        total = len(tasks_orders)
        pagination = Pagination(page=page, per_page=per_page, inner_window=1, outer_window=1, total=total, bs_version=5,  )

        offset = (page - 1) * per_page
        data_subset = get_data(tasks_orders, offset=offset, per_page=per_page)

        return render_template('cabinet_client/orders.html', pagination=pagination,
             orders=data_subset,  user=current_user)
  
 

@bp.route('/cabinet/orders/update/<int:order_id>', methods=['GET', 'POST'])
@login_required
@author_permission.require(http_exception=403)
@inject
def update(order_id, cntrl: OrderCntrl = Provide[Container.order_cntrl]): 
    session.pop('order_dto', None)
    print("order_update", order_id)
    order :OrderDTO = cntrl.load_for_order_id(order_id) # завнатаженя ордера
    print(f'order_update {order.store}')
    dto = OrderDTO.model_validate(order) # робимо ДТО
    data = OrderedProductSession.proccess(dto) # для сесії з ДТО
    try:
        session['order_dto'] = data  # сесія з dto
    except TypeError:
        flash("Помилка сесії", category="error")
        return redirect(f'/cabinet/orders/update/{order_id}') 
    if request.method == 'POST':
        saved = session.get('order_dto') # вертаємо ордер з сесії
        if not saved:
            return "Session expired", 400
        ord_mapp_sess = OrderFormMapper() # створюємо маппер для форми та сессії
        #  створюємо ДТО для model
        order_dto = ord_mapp_sess.update_order_dto_from_session(saved, request.form)
        dto = OrderDTO(**order_dto)
        order = cntrl.update_order3(order_id, dto)
        session.pop('order_dto', None)
        flash(f'Замовлення оновлено', category='success')
        return redirect(f'/cabinet/orders/update/{order_id}')        
    else:     
        admin = admin_permission.can()
        print(f"перевірка {vars(current_user.roles)}")
        return render_template(
                'cabinet_client/update_order_new.html', 
                order=order, 
                user=current_user,
                admin=admin
            )  
   
@bp.route('/cabinet/orders/add_order', methods=['POST', 'GET'])
@login_required
@author_permission.require(http_exception=403)
@inject
def add_order(cntrl: OrderCntrl = Provide[Container.order_cntrl]):      
    if request.method == 'POST': 
        print("add_order:}", request.form)
        mapper = OrderFormMapper()
        order_dto = mapper.from_request(request)
        resp = cntrl.add_order3(order_dto)
        if resp.get("add_order3") == "ok":
            order = resp.get("result")
            flash('Замовлення створено', category='success')

            return redirect(f'/cabinet/orders/update/{order.id}')
        else:
            flash('Замовлення нестворено', category='warning')
            return redirect(f'/cabinet/orders/add_order')
        
    return render_template('cabinet_client/add_order.html', user=current_user)
  


@bp.route('/cabinet/orders/confirmed/<int:id>', methods=['POST', 'GET'])
@login_required
@author_permission.require(http_exception=403)
@inject
def send_cab(id, cntrl: OrderCntrl = Provide[Container.order_cntrl]):
    if request.method == 'POST':
        return redirect('/cabinet/orders/filter/registered/10')
    else:
        try: 
            order: OrderDTO = cntrl.serv.get_by_id(id) 
            # if order.store.api in ["prom", "rozetka"]:
                # print(f"send_cab: {cntrl.client_serv.providers.keys()}")
                # client = cntrl.client_serv("evo", token_id=order.store.token)
                # # client = cntrl.client_serv.(marketplace=order.store.api, path=order.store.token_market)
                # client.print_test()
                # # print(f"Кліент готов: {client}")
            
            resp = cntrl.confirmed_order(id)
            if resp:
                flash('Замовлення підтвержено', category='success')
            else:
                flash('Замовлення підтверджено але ттн не створено: ' + resp["delivery"], category='error')
        except Exception as e:
            OC_log.exception(f"send_cab: {e}")
            flash(str(e), category='error')
            return redirect(f'/cabinet/orders/update/{id}')
        return redirect(f'/cabinet/orders/update/{id}')


@bp.route('/cabinet/orders/return/<int:id>', methods=['POST', 'GET'])
@login_required
@admin_permission.require(http_exception=403)
@inject
def return_order(id,  cntrl: OrderCntrl = Provide[Container.order_cntrl]):
    if request.method == 'POST':
        return redirect('/cabinet/orders/filter/registered/10')
    else:
        print(f"Працює {id}")
        resp = cntrl.return_order(id, 14)
        if resp == True:
            flash('Замовлення повернено', category='success')
        else:
            flash('Замовлення підтверджено але ттн не створено: ', category='error')
        return redirect('/cabinet/orders/filter/registered/10')

@bp.route('/cabinet/orders/get_cities', methods=['POST', 'GET'])
@login_required
@author_permission.require(http_exception=403)
@inject
def get_cities(cntrl: OrderCntrl = Provide[Container.order_cntrl]):
    # try:
        search_query = request.args.get('q')
        # print(count)
        city_data = fl_cl.directory_load_json("api/nova_poshta/create_data/warehouses")
        # print(city_data)
        # Фільтрація даних за текстовим запитом
        filtered_data = []
        for item in city_data["CityList"]:
            if search_query.lower() in item["City"].lower():
                word = item
                # print(word)
                filtered_data.append(item)
                # print("filtered_data", filtered_data)
        if filtered_data:  # print(f"данні отриманні {filtered_data}")
            return jsonify({'results': filtered_data})
        else:
            return jsonify({'results': []})


    # except Exception as e:
    #     OC_log.info("Помилка пошуку міста %s", e)
    #     return jsonify({'results': []})



@bp.route('/cabinet/orders/get_warehouse', methods=['POST', 'GET'])
@login_required
@author_permission.require(http_exception=403) 
def get_warehouse():
    city_ref = request.args.get('cityRef')

    # warehouse_option = request.form['warehouse_option']
    search_query = request.args.get('q', '').lower()
    cities_data = fl_cl.directory_load_json("api/nova_poshta/create_data/warehouses")

    # Фільтрація даних за текстовим запитом
    city_data = next((item for item in cities_data["CityList"] if city_ref in item["CityRef"].lower()), None)
    # print(f"дивимось {city_data}")
    if city_data:
        # Здійснити пошук відділень в даному місті
        warehouse_data = [warehouse for warehouse in city_data['Warehouse'] if search_query in warehouse['Description'].lower()]
        return jsonify({'results': warehouse_data})
    else:
        return jsonify({'results': []})

@bp.route('/cabinet/orders/get_post', methods=['POST', 'GET'])
@login_required
@author_permission.require(http_exception=403)
def get_post():
    city_ref = request.args.get('cityRef')
    search_query = request.args.get('q', '').lower()
    cities_data = fl_cl.directory_load_json("api/nova_poshta/create_data/warehouses")
    # Фільтрація даних за текстовим запитом
    city_data = next((item for item in cities_data["CityList"] if city_ref in item["CityRef"].lower()), None)
    # print(f"дивимось {city_data}")
    if city_data:
        # Здійснити пошук відділень в даному місті
        warehouse_data = [warehouse for warehouse in city_data['Post'] if search_query in warehouse['Description'].lower()]
        return jsonify({'results': warehouse_data})
    else:
        return jsonify({'results': []})

@bp.route('/cabinet/orders/get_product', methods=['POST', 'GET'])
@login_required
@author_permission.require(http_exception=403)
@inject
def get_product(product_cntrl: ProductCntrl = Provide[Container.prod_cntrl]):
    search_query = request.args.get('q', '').lower()
    items = product_cntrl.load_product_all()
    result = []
    for item in items:
        if search_query in item.article.lower() or search_query in item.product_name.lower():
            prod_data = {
                'id': item.id,
                'article': item.article + ' - ' + item.product_name
            }
            result.append(prod_data)
    if result:
        return jsonify({'results': result})
    else:
        return jsonify({'results': []})

def verify_token(token):
    valid_token = os.getenv("SEND_TO_CRM_TOKEN")
    if token == valid_token:
        return True
    return False



@bp.route('/cabinet/orders/delete/<int:id>')
@login_required
@admin_permission.require(http_exception=403)
@inject
def delete(id, cntrl: OrderCntrl = Provide[Container.order_cntrl]):
    try:
        task_to_delete = cntrl.delete_order(id)
        flash(f'Замовлення видалено', category='success')
        return redirect('/cabinet/orders/filter/registered/10')
    except:
        return 'Це замовлення вже було видаленно'


@bp.route('/cabinet/orders/dublicate/<int:id>', methods=['GET', 'POST'])
@login_required
@author_permission.require(http_exception=403)
@inject
def dublicate(
    cntrl: OrderCntrl = Provide[Container.order_cntrl], id: int = None
    ):
    order = cntrl.dublicate_v2(id)
    if order:
        flash('Замовлення дубльоване', category='success')
        return redirect(f'/cabinet/orders/update/{order.id}')
    else:
        flash('Замовлення не дубльоване', category='error')
        return redirect(f'/cabinet/orders/update/{id}')

@bp.route('/cabinet/orders/search_for_phone', methods=['POST', 'GET'])
@login_required
@author_permission.require(http_exception=403)
@inject
def search_for_phone(cntrl: OrderCntrl = Provide[Container.order_cntrl]):
    search = cntrl.search_for_phone(request)
    return search

@bp.route('/cabinet/order_draft', methods=['POST', 'GET'])
@login_required
@author_permission.require(http_exception=403)
@inject
def order_draft(
                cntrl: OrderCntrl = Provide[Container.order_cntrl],
                del_ord_cntrl: DeliveryOrderCntrl = Provide[Container.deliv_ord_cntrl]
                ):
    if request.method == 'POST':
        print(">>> Add datebase")
        print(f"order_draft {request.json}")
        bool = del_ord_cntrl.add_registr(request.json)
        if bool:
            print(f"bool {bool}")
            # flash(f'ТТН додано до реєстр', category='success')
        else:
            flash(f'Невийшло', category='error')
        return jsonify(bool)
    else:
        tasks_orders = cntrl.load_confirmed_order()
        page = request.args.get('page', default=1, type=int)
        per_page = 50
        total = len(tasks_orders)
        pagination = Pagination(page=page, per_page=per_page, total=total, css_framework='bootstrap5')
        offset = (page - 1) * per_page
        data_subset = get_data(tasks_orders, offset=offset, per_page=per_page)

        return render_template('cabinet_client/order_draft.html', 
            pagination=pagination,
            orders=data_subset,  
            user=current_user
            )

@bp.route('/cabinet/orders/del_reg', methods=['POST', 'GET'])
@login_required
@author_permission.require(http_exception=403)
def reg(del_ord_cntrl: DeliveryOrderCntrl = Provide[Container.deliv_ord_cntrl]):
    print(">>> Delete reg datebase")
    print(f"order_draft {request.json}")
    bool = del_ord_cntrl.delete_ttn_in_reg(request.json)
    if bool:
        # flash(f'Видалено з реєстру', category='success')
        return jsonify({"succes": True})
    else:
        # flash(f'Невийшло', category='error')
        return jsonify({"succes": False})
   
@bp.route('/cabinet/orders/changeStatus', methods=['POST', 'GET'])
@login_required
@author_permission.require(http_exception=403)
@inject
def changeStatus(cntrl: OrderCntrl = Provide[Container.order_cntrl]):  
    print(">>> Change status")
    print(f"order_draft {request.json}")
    bool = cntrl.change_status(request.json)
    if bool: 
        # flash(f'Змінено статус', category='success')
        return jsonify({"succes": True})
    else:  
        # flash(f'Невийшло', category='error')
        return jsonify({"succes": False})
              
@bp.route('/cabinet/orders/filter/confirmeded', methods=['POST', 'GET'])
@login_required
@author_permission.require(http_exception=403)     
@inject  
def confirmeded(cntrl: OrderCntrl = Provide[Container.order_cntrl]):  
    tasks_orders = cntrl.load_confirmed_order()
    page = request.args.get('page', default=1, type=int)
    per_page = 50  
    total = len(tasks_orders) 
    pagination = Pagination(page=page, per_page=per_page, total=total, css_framework='bootstrap5')
    offset = (page - 1) * per_page
    data_subset = get_data(tasks_orders, offset=offset, per_page=per_page)

    return render_template('cabinet_client/order_draft.html', pagination=pagination,
        orders=data_subset, user=current_user)

@bp.route('/cabinet/orders/filter/registered/<int:id>', methods=['POST', 'GET'])
@login_required 
@author_permission.require(http_exception=403)
@inject 
def registered(id, cntrl: OrderCntrl = Provide[Container.order_cntrl]):
    tasks_orders = cntrl.load_status_id(id)

    page = request.args.get('page', default=1, type=int)
    per_page = 50 
    total = len(tasks_orders)
    pagination = Pagination(page=page, per_page=per_page, total=total, css_framework='bootstrap5')
    offset = (page - 1) * per_page
    data_subset = get_data(tasks_orders, offset=offset, per_page=per_page)

    return render_template('cabinet_client/order_draft.html', pagination=pagination,
                            orders=data_subset, user=current_user)

@bp.route('/cabinet/orders/send_storage/<int:id>', methods=['GET', 'POST'])
@login_required
@author_permission.require(http_exception=403)
@inject
def send_storage(id, cntrl: OrderCntrl = Provide[Container.order_cntrl]):
    resp = cntrl.send_storage(id)
    return jsonify({"success": True})


@bp.route('/cabinet/orders/test/<int:id>', methods=['GET', 'POST'])
@login_required
@author_permission.require(http_exception=403)
@inject
def test_order(id, cntrl: OrderCntrl = Provide[Container.order_cntrl]):
    resp = cntrl.test_order(id)
    print(resp)
    return jsonify({"error": resp[1], "success": resp[0]})
 
@bp.route('/cabinet/orders/change_history', methods=['POST', 'GET'])
@login_required 
@author_permission.require(http_exception=403)
@inject
def change_history(order_cntrl: 
        OrderCntrl = Provide[Container.order_cntrl]):
    if request.method == 'POST':
        resp = order_cntrl.change_history(request)
        responce_data = {'status': 'success', 'message': 'False'}
        if resp == True: 
            responce_data['message'] = "Success"
            return jsonify(responce_data)
        else:
            return jsonify(responce_data)

    return render_template('cabinet_client/Products/add_product.html', user=current_user )



#  id |        name        | description
# ----+--------------------+-------------
#   1 | Підтвердити        |
#   2 | Підтвержено        |
#   3 | Оплачено           |
#   4 | Несплачено         |
#   5 | Скасовано          |
#   6 | Предзамовлення     |
#   7 | Питання            |
#   8 | Відправлено        |
#   9 | Отримано           |
#  10 | Нове               |
#  11 | Очікує відправленя |
#  12 | Виконано           |
#  13 | Тест
#  14 | Повернення

#  id | name |                               description                               | code
# ----+------+-------------------------------------------------------------------------+------
#   1 |      | Відправник самостійно створив цю накладну, але ще не надав до відправки |    1
#   2 |      | Видалено                                                                |    2
#   3 |      | Прибув на відділення                                                    |    7
#   4 |      | Відправлення отримано                                                   |    9
#   5 |      | На шляху до одержувача                                                  |  101
#   6 |      | Відмова одержувача (отримувач відмовився від відправлення)              |  103
# https://api.telegram.org/bot603175634:AAHNHBKy56g37S1WiS1KZuw_a-aZjahqD7o/getFile?file_id=AgACAgIAAxkBAAIMl2YWFuaONHD9_7SWvzDiiK8vmNQSAAK31jEbGsoISBKbThvzHGUpAQADAgADbQADNAQ

#  id |         name         | description
# ----+----------------------+-------------
#   1 | Нова Пошта           |
#   3 | Укрпошта             |
#   5 | Самовивіз            |
#   4 | Meest                |
#   2 | Точка видачі Rozetka |

 #    id = db.Column(db.Integer, primary_key=True)
 #    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
 #    phone = db.Column(db.String(50))
 #    ttn = db.Column(db.String(50))
 #    ttn_ref = db.Column(db.String(50))
 #    client_firstname = db.Column(db.String(50))
 #    client_lastname = db.Column(db.String(50))
 #    client_surname = db.Column(db.String(50))
 #    delivery_option = db.Column(db.String(50))
 #    city_name = db.Column(db.String(50))
 #    city_ref = db.Column(db.String(50))
 #    region = db.Column(db.String(50))
 #    area = db.Column(db.String(50))
 #    warehouse_option = db.Column(db.String(50))
 #    warehouse_text = db.Column(db.String(255))
 #    warehouse_ref = db.Column(db.String(50))
 #    payment_option = db.Column(db.String(50))
 #    ordered_product = db.relationship('OrderedProduct', backref='orders', cascade='all, delete-orphan')
 #    telegram_ordered = db.relationship('TelegramOrdered', backref='orders', cascade='all, delete-orphan')
 #    products = db.relationship('Products', secondary='ordered_product', overlaps="ordered_product,orders")
 #    sum_price = db.Column(db.Float)
 #    sum_before_goods = db.Column(db.Float)
 #    description = db.Column(db.String(300))
 #    description_delivery = db.Column(db.String(50))
 #    cpa_commission = db.Column(db.String(50))
 #    client_id = db.Column(db.Integer)
 #    send_time = db.Column(db.DateTime)
 #    order_id_sources = db.Column(db.String(50))
 #    order_code = db.Column(db.String(50), unique=True)
 #    delivery_order = db.relationship("DeliveryOrder", back_populates="orders", uselist=False, cascade="all, delete-orphan")
 #    prompay_status = db.relationship("PrompayStatus", back_populates="orders")
 #    prompay_status_id = db.Column(db.Integer, db.ForeignKey(
 #        'prompay_status.id', name='fk_orders_prompay_status_id'))
 #    ordered_status = db.relationship("OrderedStatus", back_populates="orders")
 #    ordered_status_id = db.Column(db.Integer, db.ForeignKey(
 #        'ordered_status.id', name='fk_orders_ordered_status_id'))
 #    warehouse_method = db.relationship("WarehouseMethod", back_populates="orders")
 #    warehouse_method_id = db.Column(db.Integer, db.ForeignKey(
 #        'warehouse_method.id', name='fk_orders_warehouse_method_id'))
 #    source_order = db.relationship("SourceOrder", back_populates="orders")
 #    source_order_id = db.Column(db.Integer, db.ForeignKey(
 #        'source_order.id', name='fk_orders_source_order_id'))
 #    payment_method = db.relationship("PaymentMethod", back_populates="orders")
 #    payment_method_id = db.Column(db.Integer, db.ForeignKey(
 #        'payment_method.id', name='fk_orders_payment_method_id'))
 #    delivery_method = db.relationship("DeliveryMethod", back_populates="orders")
 #    delivery_method_id = db.Column(db.Integer, db.ForeignKey(
 #        'delivery_method.id', name='fk_orders_delivery_method_id'))

 #    author_id = db.Column(db.Integer, db.ForeignKey(
 #        'users.id', name='fk_orders_users_id', ondelete="CASCADE"), nullable=True)
 #    comments = db.relationship('Comment', backref='orders', passive_deletes=True)
 #    likes = db.relationship('Likes', backref='orders', passive_deletes=True)