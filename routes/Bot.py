from flask import Blueprint, render_template, request, jsonify
import os
from flask_login import current_user
from dotenv import load_dotenv
from black.tg_answer_cntrl import TgAnswerCntrl
from black.order_cntrl import OrderCntrl
from dependency_injector.wiring import inject, Provide
from infrastructure.container import Container    



load_dotenv()
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
bp = Blueprint('Bot', __name__, template_folder='templates')


@bp.route("/bot", methods=['POST', 'GET'])
@inject
def bot(order_cntrl: 
        OrderCntrl = Provide[Container.order_cntrl]
        ):
    if request.method == 'POST':
        tg = TgAnswerCntrl(order_cntrl)
        data = request.json
        try:
            tg.await_tg_button(data)
            return {'success': True}
        except:
            return {'success': False}
        
    return render_template('index.html', user=current_user)

# @bp.route("/bot_send", methods=['POST', 'GET'])
# def bot_send():
#     tg_cntrl.sendPhoto()
#     return jsonify({'success': True})

