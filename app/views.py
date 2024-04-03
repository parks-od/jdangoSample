from decimal import Decimal

from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render
from pykrx import stock
import pandas as pd
from datetime import datetime
from app.models import Asset
import json


# Create your views here.
def index(request: HttpRequest) -> HttpResponse:
    qs = Asset.objects.all()
    return render(
        request,
        "app/index.html",
        {
            "asset_list": qs,
        },
    )


def calc_asset(request):
    post_data = json.loads(request.body.decode("utf-8"))
    input_code = post_data.get("code")

    input_price = Decimal(post_data.get("price"))

    qs = Asset.objects.filter(code=input_code).first()

    clac = qs.price

    # 수익률 연산
    per_cen = round((1 - clac / input_price), 4) * 100
    print(per_cen)
    msg = ''

    if round(per_cen, 1) > 1:
        msg = f'현재 가격 {clac} 에서 {round(per_cen, 2)}% 하락할 경우 해당 금액 입니다.'
    elif clac == input_price:
        msg = "현재 가격과 일치 합니다"
    else:
        msg = f"현재 가격 {clac}에서 {round(abs(per_cen), 2)}% 상승할 경우 해당 금액 입니다."
    data = {
        "msg": msg,
    }
    return JsonResponse(data)


def get_stocks(request):
    post_data = json.loads(request.body.decode("utf-8"))
    input_code = post_data.get("parentCode")

    qs = list(Asset.objects.filter(parentCode=input_code).values("title", "code"))

    data = {
        "stocks": qs,
    }

    return JsonResponse(data)


def import_asset():
    # 기본 세팅 일별로 15:35분 스케줄링작업
    stock_name = []
    stock_code = []

    dt = datetime.now().strftime("%Y%m%d")

    # 명칭, 코드 리스트 저장
    for ticker in stock.get_market_ticker_list():
        stock_name.append(stock.get_market_ticker_name(ticker))
        stock_code.append(ticker)

    # 금일기준 등록된 값 불러오기
    today = stock.get_market_ohlcv(dt)

    # if today.empty:
    # return

    # 명칭, 코드 리스트, 등록값 데이터 정규화
    df = pd.DataFrame(
        data=list(zip(stock_name, stock_code)), columns=["종목명", "티커"]
    )
    df = pd.merge(left=today, right=df, how="inner", on="티커")
    df = df.rename(columns={"티커": "종목코드"})
    df = df[
        [
            "종목명",
            "종목코드",
            "종가",
            "등락률",
        ]
    ]

    for index, row in df.iterrows():
        Asset(parentCode='kospi', title=row['종목명'], price=row['종가'], code=row['종목코드'], today_range=row['등락률']).save()

    print(f'insert {len(df)} data was successfully saved!')
