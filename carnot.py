import numpy as np

class CarnotEngine:
    def __init__(self, TH, TC, gamma=1.4, V1=1.0, V2=2.0):
        self.TH = TH
        self.TC = TC
        self.gamma = gamma
        self.V1 = V1
        self.V2 = V2
        self._compute_states()

    def _compute_states(self):
        # 단열 과정 관계식: T * V^(gamma-1) = Constant
        # T_H * V2^(g-1) = T_C * V3^(g-1)
        ratio = (self.TH / self.TC)**(1 / (self.gamma - 1))
        self.V3 = self.V2 * ratio
        self.V4 = self.V1 * ratio

    def pv_curves(self, n=300):
        """
        P-V 그래프를 그리기 위한 데이터를 반환합니다.
        각 단계별로 (부피 배열, 압력 배열, 레이블) 튜플을 리스트로 반환합니다.
        """
        V1, V2, V3, V4 = self.V1, self.V2, self.V3, self.V4
        g = self.gamma

        # 1. 등온 팽창 (Isothermal Expansion): 1 -> 2
        V_iso_hot = np.linspace(V1, V2, n)
        P_iso_hot = self.TH / V_iso_hot

        # 2. 단열 팽창 (Adiabatic Expansion): 2 -> 3
        V_ad_exp = np.linspace(V2, V3, n)
        C_exp = self.TH * V2**(g - 1)  # PV^g = const
        P_ad_exp = C_exp / V_ad_exp**g

        # 3. 등온 압축 (Isothermal Compression): 3 -> 4
        # 그래프 연결을 위해 V3에서 V4 방향으로 생성
        V_iso_cold = np.linspace(V3, V4, n)
        P_iso_cold = self.TC / V_iso_cold

        # 4. 단열 압축 (Adiabatic Compression): 4 -> 1
        # 그래프 연결을 위해 V4에서 V1 방향으로 생성
        V_ad_comp = np.linspace(V4, V1, n)
        C_comp = self.TC * V4**(g - 1)
        P_ad_comp = C_comp / V_ad_comp**g

        return [
            (V_iso_hot, P_iso_hot, "1→2: 등온 팽창 (고온)"),
            (V_ad_exp, P_ad_exp, "2→3: 단열 팽창"),
            (V_iso_cold, P_iso_cold, "3→4: 등온 압축 (저온)"),
            (V_ad_comp, P_ad_comp, "4→1: 단열 압축")
        ]
    
        

    def efficiency(self):
        """이론 효율 계산"""
        if self.TH == 0: return 0
        return 1 - self.TC / self.TH
    
    def work_done(self):
        """카르노 사이클이 한 총 일의 양(면적)을 계산합니다."""
        # W = (TH - TC) * ln(V2/V1)
        import numpy as np
        return (self.TH - self.TC) * np.log(self.V2 / self.V1)
    