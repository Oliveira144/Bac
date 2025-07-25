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
        
        if hasattr(self, 'last_prediction'):
            self._update_stats(result)
            self._update_win_rate()

    def _update_win_rate(self):
        if self.prediction_stats['total'] > 0:
            self.prediction_stats['win_rate'] = (
                self.prediction_stats['wins'] / self.prediction_stats['total'] * 100
            )

    def _update_stats(self, actual_result: str):
        if self.last_prediction['prediction'] == actual_result:
            self.prediction_stats['wins'] += 1
        self.prediction_stats['total'] += 1
        self.last_predictions.append({
            'predicted': self.last_prediction['prediction'],
            'actual': actual_result,
            'confidence': self.last_prediction['confidence']
        })

    def predict_next(self) -> Dict:
        if len(self.game_history) < 5:
            return {'prediction': None, 'confidence': 0, 'reason': 'Histórico insuficiente'}
        
        try:
            quantum = self._analyze_quantum_pattern()
            fibonacci = self._analyze_dynamic_fibonacci()
            pressure = self._analyze_pressure_points()
            
            predictions = [
                {'method': quantum, 'weight': 0.45},
                {'method': fibonacci, 'weight': 0.35},
                {'method': pressure, 'weight': 0.20}
            ]
            
            valid_preds = [p for p in predictions if p['method']['prediction'] is not None]
            
            if not valid_preds:
                return self._smart_fallback()
            
            final_pred = self._aggregate_predictions(valid_preds)
            final_pred = self._apply_bayesian_correction(final_pred)
            
            self.last_prediction = final_pred
            return final_pred
            
        except Exception as e:
            return {'prediction': None, 'confidence': 0, 'reason': f'Erro: {str(e)}'}

    def _analyze_quantum_pattern(self) -> Dict:
        last_15 = self.game_history[-15:]
        player_count = last_15.count('PLAYER')
        banker_count = last_15.count('BANKER')
        
        diff = abs(player_count - banker_count)
        if diff >= self.quantum_threshold:
            prediction = 'BANKER' if player_count > banker_count else 'PLAYER'
            return {
                'prediction': prediction,
                'confidence': min(90, 75 + diff * 2),
                'reason': f'Oscilação Quântica (Δ={diff})'
            }
        
        last_5 = last_15[-5:]
        if len(set(last_5)) == 1:
            return {
                'prediction': 'BANKER' if last_5[0] == 'PLAYER' else 'PLAYER',
                'confidence': 89,
                'reason': f'Entrelaçamento Quântico (5x {last_5[0]})'
            }
        
        return {'prediction': None, 'confidence': 0, 'reason': ''}

    def _analyze_dynamic_fibonacci(self) -> Dict:
        last_10 = self.game_history[-10:]
        numeric = [2 if x == 'PLAYER' else 3 if x == 'BANKER' else 5 for x in last_10]
        
        for i in range(len(self.fibonacci_sequence) - 2):
            fib_seq = self.fibonacci_sequence[i:i+3]
            if ','.join(map(str, fib_seq)) in ','.join(map(str, numeric)):
                next_val = self.fibonacci_sequence[i+3] if i+3 < len(self.fibonacci_sequence) else 3
                prediction = 'PLAYER' if next_val == 2 else 'BANKER' if next_val == 3 else 'TIE'
                return {
                    'prediction': prediction,
                    'confidence': 83 + (i * 2),
                    'reason': f'Fibonacci Dinâmico ({fib_seq})'
                }
        
        return {'prediction': None, 'confidence': 0, 'reason': ''}

    def _analyze_pressure_points(self) -> Dict:
        total = len(self.game_history)
        
        for point in self.pressure_points:
            if total % point == 0 and total >= point:
                last_n = self.game_history[-point:]
                p_count = last_n.count('PLAYER')
                b_count = last_n.count('BANKER')
                
                prediction = 'BANKER' if p_count > b_count else 'PLAYER'
                return {
                    'prediction': prediction,
                    'confidence': 85 + min(10, abs(p_count - b_count)),
                    'reason': f'Ponto de Pressão (múltiplo de {point})'
                }
        
        return {'prediction': None, 'confidence': 0, 'reason': ''}

    def _aggregate_predictions(self, predictions: List[Dict]) -> Dict:
        pred_counts = {}
        total_weight = 0
        
        for pred in predictions:
            method = pred['method']
            weight = pred['weight']
            
            if method['prediction'] not in pred_counts:
                pred_counts[method['prediction']] = {
                    'confidence': 0,
                    'reasons': [],
                    'weight': 0
                }
            
            pred_counts[method['prediction']]['confidence'] += method['confidence'] * weight
            pred_counts[method['prediction']]['reasons'].append(method['reason'])
            pred_counts[method['prediction']]['weight'] += weight
            total_weight += weight
        
        final_pred = max(pred_counts.items(), key=lambda x: x[1]['weight'])
        
        return {
            'prediction': final_pred[0],
            'confidence': final_pred[1]['confidence'] / final_pred[1]['weight'],
            'reason': ' | '.join(final_pred[1]['reasons'])
        }

    def _apply_bayesian_correction(self, prediction: Dict) -> Dict:
        if len(self.game_history) < 50:
            return prediction
        
        last_100 = self.game_history[-100:]
        p_ratio = last_100.count('PLAYER') / len(last_100)
        b_ratio = last_100.count('BANKER') / len(last_100)
        
        if prediction['prediction'] == 'PLAYER' and p_ratio > 0.52:
            return {
                **prediction,
                'confidence': max(75, prediction['confidence'] * 0.95),
                'reason': prediction['reason'] + ' | Correção Bayesiana (PLAYER super-representado)'
            }
        
        if prediction['prediction'] == 'BANKER' and b_ratio > 0.52:
            return {
                **prediction,
                'confidence': max(75, prediction['confidence'] * 0.95),
                'reason': prediction['reason'] + ' | Correção Bayesiana (BANKER super-representado)'
            }
        
        return prediction

    def _smart_fallback(self) -> Dict:
        last_10 = self.game_history[-10:]
        p_count = last_10.count('PLAYER')
        b_count = last_10.count('BANKER')
        
        if p_count < 3:
            return {'prediction': 'PLAYER', 'confidence': 65, 'reason': 'Correção: PLAYER sub-representado'}
        if b_count < 3:
            return {'prediction': 'BANKER', 'confidence': 65, 'reason': 'Correção: BANKER sub-representado'}
        
        return {'prediction': 'BANKER', 'confidence': 58, 'reason': 'Vantagem estatística padrão'}

    def get_stats(self) -> Dict:
        stats = {
            'win_rate': round(self.prediction_stats.get('win_rate', 0), 1),
            'wins': self.prediction_stats.get('wins', 0),
            'total': self.prediction_stats.get('total', 0),
            'recent_predictions': list(self.last_predictions)
        }
        
        if stats['total'] > 10:
            last_10 = self.last_predictions[-10:]
            stats['recent_win_rate'] = round(
                sum(1 for p in last_10 if p['predicted'] == p['actual']) / len(last_10) * 100, 1
            ) if last_10 else 0
            
        return stats

    def reset(self):
        self.game_history = []
        self.prediction_stats = {'wins': 0, 'total': 0, 'win_rate': 0.0}
        self.last_predictions = deque(maxlen=20)
        if hasattr(self, 'last_prediction'):
            del self.last_prediction

# Configuração do Streamlit
st.set_page_config(
    page_title="Bac Bo Quantum Predictor",
    page_icon="🎲",
    layout="wide"
)

# Inicialização do predictor na sessão
if 'predictor' not in st.session_state:
    st.session_state.predictor = BacBoPredictor()

# Interface do usuário
st.title("🎲 Bac Bo Quantum Predictor")
st.markdown("Sistema avançado de previsão com algoritmos quânticos e Fibonacci dinâmico")

col1, col2 = st.columns([3, 2])

with col1:
    st.header("📊 Controle do Jogo")
    
    result = st.radio("Último resultado:", ["PLAYER", "BANKER", "TIE"], horizontal=True)
    
    col1_1, col1_2, col1_3 = st.columns(3)
    with col1_1:
        if st.button("✅ Registrar Resultado"):
            st.session_state.predictor.add_result(result)
            st.success(f"Resultado {result} registrado!")
    with col1_2:
        if st.button("🔄 Reiniciar Sistema"):
            st.session_state.predictor.reset()
            st.success("Sistema reiniciado!")
    with col1_3:
        if st.button("🔮 Fazer Previsão"):
            prediction = st.session_state.predictor.predict_next()
            st.session_state.last_prediction = prediction
    
    if 'last_prediction' in st.session_state:
        pred = st.session_state.last_prediction
        st.subheader("🎯 Próxima Aposta Recomendada")
        
        if pred['prediction']:
            confidence_color = "green" if pred['confidence'] > 70 else "orange" if pred['confidence'] > 55 else "red"
            
            st.markdown(f"""
            <div style="background-color:#1e1e1e;padding:20px;border-radius:10px;border-left:5px solid {confidence_color}">
                <h2 style="color:white;margin-top:0;">Próxima aposta: <span style="color:{'blue' if pred['prediction']=='PLAYER' else 'red' if pred['prediction']=='BANKER' else 'purple'}">{pred['prediction']}</span></h2>
                <p style="color:white;">Confiança: <span style="color:{confidence_color}">{pred['confidence']:.1f}%</span></p>
                <p style="color:#aaa;">{pred['reason']}</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.warning("Não foi possível fazer uma previsão confiável")

with col2:
    st.header("📈 Estatísticas")
    
    stats = st.session_state.predictor.get_stats()
    
    st.metric("Taxa de Acerto Global", f"{stats['win_rate']:.1f}%")
    st.metric("Total de Previsões", stats['total'])
    st.metric("Previsões Corretas", stats['wins'])
    
    if 'recent_win_rate' in stats:
        st.metric("Taxa de Acerto Recente", f"{stats['recent_win_rate']:.1f}%")
    
    st.subheader("Últimas Previsões")
    if stats['recent_predictions']:
        for i, pred in enumerate(stats['recent_predictions'][-5:], 1):
            status = "✅" if pred['predicted'] == pred['actual'] else "❌"
            st.write(f"{i}. {pred['predicted']} → {pred['actual']} {status} (Conf: {pred['confidence']:.1f}%)")
    else:
        st.info("Nenhuma previsão registrada ainda")

st.header("📜 Histórico Completo")
if st.session_state.predictor.game_history:
    history_text = " ".join([
        f"<span style='color:{'blue' if x=='PLAYER' else 'red' if x=='BANKER' else 'purple'}'>{x[0]}</span>" 
        for x in st.session_state.predictor.game_history[-50:]
    ])
    st.markdown(f"<div style='font-family:monospace;'>{history_text}</div>", unsafe_allow_html=True)
    st.caption(f"Total de jogos: {len(st.session_state.predictor.game_history)}")
else:
    st.info("Nenhum resultado registrado ainda")
