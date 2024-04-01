import sched
from decimal import Decimal

from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render
from pykrx import stock
import pandas as pd
from datetime import datetime
from app.models import Asset


# Create your views here.
def index(request: HttpRequest) -> HttpResponse:
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
    qs = Asset.objects.all()
    return render(
        request,
        "app/index.html",
        {
            "asset_list": qs,
        },
    )


def import_asset():
    print('hi')


def calc_asset(request):
    input_code = request.GET.get("code")
    input_price = Decimal(request.GET.get("price"))

    qs = Asset.objects.filter(code=input_code).first()

    clac = qs.price

    # 수익률 연산
    per_cen = round((1 - clac / input_price), 4) * 100

    if round(per_cen, 1) > 1:
        print("현재 가격(%.2f)에서 %.2f %% 하락할 경우 해당 금액 입니다." % clac.per_cen)
    elif clac == input_price:
        print("현재 가격과 일치 합니다")
    else:
        print("현재 가격(%.2f)에서 %.2f %% 상승할 경우 해당 금액 입니다." % (clac, abs(per_cen)))
    return JsonResponse(clac)


def get_stocks(request):
    input_code = request.GET.get("parentCode")

    qs = Asset.objects.filter(parentCode=input_code)

    for stock in qs:
        print(stock)
        
    return JsonResponse(qs)