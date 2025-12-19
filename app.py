import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import platform
import matplotlib as mpl
from carnot import CarnotEngine  

# 1. 디자인 및 폰트 설정
def set_design():
    # Streamlit Cloud(Linux) 환경을 고려하여 폰트 에러 방지
    try:
        system_name = platform.system()
        if system_name == "Windows":
            mpl.rc('font', family='Malgun Gothic')
        elif system_name == "Darwin":
            mpl.rc('font', family='AppleGothic')
        else:
            # 리눅스 서버에서는 기본적으로 영문을 쓰고 한글 깨짐 방지만 설정
            mpl.rc('font', family='DejaVu Sans') 
    except:
        pass
    mpl.rc('axes', unicode_minus=False)
    plt.style.use('default')

set_design()

st.set_page_config(page_title="카르노 사이클 분석기", layout="wide")

# 헤더 섹션
st.title("카르노 기관 ")
st.divider()

col1, col2 = st.columns([1, 2], gap="large")

with col1:

    st.subheader("시뮬레이션 설정")
    
    # 입력 슬라이더
    TH = st.slider("고온부 온도 $T_H$ (K)", 300, 1500, 600, step=10)
    TC = st.slider("저온부 온도 $T_C$ (K)", 100, TH-10, 300, step=10)
    
    # 엔진 인스턴스 생성
    engine = CarnotEngine(TH, TC)
    
    # 데이터 계산
    eta = engine.efficiency() * 100
    work = engine.work_done()
    qh = engine.TH * np.log(engine.V2/engine.V1) # 흡수 열량
    qc = qh - work # 방출 열량

    # 분석 결과 지표 (디자인 강화)
    st.subheader("성능 지표")
    c1, c2 = st.columns(2)
    c1.metric(label="카르노 효율 ($\eta$)", value=f"{eta:.1f}%")
    c2.metric(label="총 한 일 ($W$)", value=f"{work:.2f} J")

    st.info(f"""
    **Cycle Info:**
    - 최대 부피 (V3): {engine.V3:.2f}
    - 흡수 열량 (QH): {engine.TH * np.log(engine.V2/engine.V1):.2f} J
    """)


with col2:
    # 그래프 생성
    fig, ax = plt.subplots(figsize=(10, 7))
    curves = engine.pv_curves()
    
    # 색상 테마
    colors = ['#d62728', '#ff7f0e', '#1f77b4', '#2ca02c']
    labels = ['등온 팽창 ($T_H$)', '단열 팽창', '등온 압축 ($T_C$)', '단열 압축']

    # 2. 각 과정 선 그리기
    for i, (V, P, _) in enumerate(curves):
        ax.plot(V, P, label=labels[i], color=colors[i], linewidth=3)
        
        # 화살표 추가
        mid = len(V) // 2
        ax.annotate('', xy=(V[mid+2], P[mid+2]), xytext=(V[mid], P[mid]),
                    arrowprops=dict(arrowstyle="->", color=colors[i], lw=2))

    # 그래프 디테일
    ax.set_xlabel("부피 $V$ (Volume)", fontsize=12)
    ax.set_ylabel("압력 $P$ (Pressure)", fontsize=12)
    ax.set_title(f"P-V Diagram", fontsize=15, pad=20)
    ax.legend(loc='upper right', frameon=True, facecolor='white')
    ax.grid(True, linestyle=':', alpha=0.6)

    st.pyplot(fig)