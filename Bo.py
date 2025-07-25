import streamlit as st
from collections import deque
import numpy as np
from typing import List, Dict

class BacBoPredictor:
    def __init__(self):
        self.game_history = []
        self.prediction_stats = {'wins': 0, 'total': 0, 'win_rate': 0.0}
        self.last_predictions = deque(maxlen=20)
        self.quantum_threshold = 7
        self.fibonacci_sequence = [2, 3, 5, 8, 13, 21, 34]
        self.pressure_points = [5, 7, 10, 15, 20, 25, 30]

    def add_result(self, result: str):
        result = result.upper()
        if result not in ['PLAYER', 'BANKER', 'TIE']:
            raise ValueError("Resultado inválido")
        self.game_history.append(result)
        
        # Faz previsão automática após cada resultado
        if len(self.game_history) >= 5:
            self.last_prediction = self.predict_next()
            
            # Atualiza estatísticas se houver previsão anterior para comparar
            if len(self.game_history) > 5:
                self._update_stats(result)
                self._update_win_rate()

    # [...] (Manter todas as outras funções da classe BacBoPredictor como no código anterior)

# Configuração do Streamlit
st.set_page_config(
    page_title="Bac Bo Predictor PRO",
    page_icon="🎲",
    layout="centered"
)

# Inicialização do predictor na sessão
if 'predictor' not in st.session_state:
    st.session_state.predictor = BacBoPredictor()

# CSS personalizado para as bolinhas do histórico
st.markdown("""
<style>
.history-container {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    margin-bottom: 20px;
}
.history-item {
    width: 24px;
    height: 24px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    color: white;
    font-weight: bold;
    font-size: 12px;
}
.player {
    background-color: #3b82f6;
}
.banker {
    background-color: #ef4444;
}
.tie {
    background-color: #a855f7;
}
.prediction-card {
    border-radius: 10px;
    padding: 15px;
    margin-bottom: 20px;
    border-left: 5px solid;
}
.high-confidence {
    border-color: #10b981;
    background-color: #064e3b20;
}
.medium-confidence {
    border-color: #f59e0b;
    background-color: #92400e20;
}
.low-confidence {
    border-color: #ef4444;
    background-color: #7f1d1d20;
}
</style>
""", unsafe_allow_html=True)

# Interface do usuário
st.title("🎲 Bac Bo Predictor PRO")
st.markdown("Sistema automático de previsão com histórico visual")

# Controles principais
col1, col2, col3 = st.columns(3)
with col1:
    result = st.selectbox("Resultado atual:", ["PLAYER", "BANKER", "TIE"])
with col2:
    if st.button("✅ Registrar", help="Registra o resultado e gera nova previsão"):
        st.session_state.predictor.add_result(result)
        st.rerun()
with col3:
    if st.button("🔄 Reiniciar", help="Limpa todo o histórico"):
        st.session_state.predictor.reset()
        st.rerun()

# Exibição do histórico visual
st.subheader("Histórico de Resultados")
if st.session_state.predictor.game_history:
    history_html = "<div class='history-container'>"
    for i, result in enumerate(st.session_state.predictor.game_history):
        cls = "player" if result == "PLAYER" else "banker" if result == "BANKER" else "lie"
        history_html += f"<div class='history-item {cls}'>{result[0]}</div>"
    history_html += "</div>"
    st.markdown(history_html, unsafe_allow_html=True)
else:
    st.info("Nenhum resultado registrado ainda")

# Previsão automática
if len(st.session_state.predictor.game_history) >= 5 and hasattr(st.session_state.predictor, 'last_prediction'):
    pred = st.session_state.predictor.last_prediction
    if pred['prediction']:
        # Determina a classe CSS baseado na confiança
        if pred['confidence'] >= 70:
            confidence_class = "high-confidence"
            confidence_text = "Alta confiança"
        elif pred['confidence'] >= 55:
            confidence_class = "medium-confidence"
            confidence_text = "Média confiança"
        else:
            confidence_class = "low-confidence"
            confidence_text = "Baixa confiança"
        
        # Cor do texto baseado no tipo de previsão
        pred_color = "blue" if pred['prediction'] == "PLAYER" else "red" if pred['prediction'] == "BANKER" else "purple"
        
        st.markdown(f"""
        <div class="prediction-card {confidence_class}">
            <h3 style="margin-top:0;color:{pred_color};">Próxima aposta: {pred['prediction']}</h3>
            <p><strong>Confiança:</strong> {pred['confidence']:.1f}% ({confidence_text})</p>
            <p><strong>Lógica:</strong> {pred['reason']}</p>
        </div>
        """, unsafe_allow_html=True)

# Estatísticas
stats = st.session_state.predictor.get_stats()
if stats['total'] > 0:
    st.subheader("📊 Estatísticas de Desempenho")
    
    col_stat1, col_stat2, col_stat3 = st.columns(3)
    with col_stat1:
        st.metric("Taxa de Acerto", f"{stats['win_rate']:.1f}%")
    with col_stat2:
        st.metric("Previsões Corretas", stats['wins'])
    with col_stat3:
        st.metric("Total de Previsões", stats['total'])
    
    if 'recent_win_rate' in stats:
        st.metric("Acerto Recente (últimas 10)", f"{stats['recent_win_rate']:.1f}%")

# Instruções
with st.expander("ℹ️ Como usar"):
    st.markdown("""
    1. Selecione o resultado atual (Player, Banker ou Tie)
    2. Clique em **Registrar** para adicionar ao histórico
    3. O sistema automaticamente gerará a próxima previsão
    4. O histórico é exibido visualmente com bolinhas coloridas
    5. Reinicie quando quiser começar um novo jogo
    
    **Cores do histórico:**
    - 🔵 Azul: Player
    - 🔴 Vermelho: Banker
    - 🟣 Roxo: Tie
    """)

# Rodapé
st.markdown("---")
st.caption("Sistema Bac Bo Predictor PRO v5.0 - Algoritmo quântico com Fibonacci dinâmico")
