import numpy as np
from collections import deque
from typing import List, Dict, Optional, Tuple

class BacBoQuantumPredictor:
    def __init__(self, window_size: int = 100):
        self.game_history = []
        self.window_size = window_size
        self.prediction_stats = {'wins': 0, 'total': 0}
        self.last_predictions = deque(maxlen=20)
        
        # Parâmetros ajustáveis
        self.quantum_threshold = 8
        self.fibonacci_sequence = [2, 3, 5, 8, 13, 21]
        self.pressure_points = [7, 10, 15, 20, 25, 30]

    def add_result(self, result: str):
        """Adiciona um novo resultado ao histórico"""
        if result not in ['PLAYER', 'BANKER', 'TIE']:
            raise ValueError("Resultado inválido. Use 'PLAYER', 'BANKER' ou 'TIE'")
            
        self.game_history.append(result)
        
        # Atualiza estatísticas se houver uma previsão anterior
        if hasattr(self, 'last_prediction'):
            self._update_stats(result)
    
    def predict_next(self) -> Dict:
        """Faz a previsão do próximo resultado"""
        if len(self.game_history) < 5:
            return {'prediction': None, 'confidence': 0, 'reason': 'Histórico insuficiente'}
        
        # 1. Análise Quântica
        quantum = self._analyze_quantum_pattern()
        
        # 2. Fibonacci Dinâmico
        fibonacci = self._analyze_dynamic_fibonacci()
        
        # 3. Pontos de Pressão
        pressure = self._analyze_pressure_points()
        
        # Combinação ponderada
        predictions = [
            {'method': quantum, 'weight': 0.40},
            {'method': fibonacci, 'weight': 0.35},
            {'method': pressure, 'weight': 0.25}
        ]
        
        # Filtra previsões válidas
        valid_preds = [p for p in predictions if p['method']['prediction'] is not None]
        
        if not valid_preds:
            return self._smart_fallback()
        
        # Agrega previsões
        final_pred = self._aggregate_predictions(valid_preds)
        
        # Aplica correção bayesiana
        final_pred = self._apply_bayesian_correction(final_pred)
        
        self.last_prediction = final_pred
        return final_pred
    
    def _analyze_quantum_pattern(self) -> Dict:
        """Padrão de oscilação quântica"""
        last_15 = self.game_history[-15:]
        player_count = last_15.count('PLAYER')
        banker_count = last_15.count('BANKER')
        
        # Oscilação quântica
        diff = abs(player_count - banker_count)
        if diff >= self.quantum_threshold:
            prediction = 'BANKER' if player_count > banker_count else 'PLAYER'
            return {
                'prediction': prediction,
                'confidence': min(90, 75 + diff * 2),
                'reason': f'Oscilação Quântica (Δ={diff})'
            }
        
        # Padrão de entrelaçamento
        last_5 = last_15[-5:]
        if len(set(last_5)) == 1:  # Todos iguais
            return {
                'prediction': 'BANKER' if last_5[0] == 'PLAYER' else 'PLAYER',
                'confidence': 89,
                'reason': f'Entrelaçamento Quântico (5x {last_5[0]})'
            }
        
        return {'prediction': None, 'confidence': 0, 'reason': ''}
    
    def _analyze_dynamic_fibonacci(self) -> Dict:
        """Sequência Fibonacci dinâmica aplicada ao Bac Bo"""
        last_10 = self.game_history[-10:]
        numeric = [2 if x == 'PLAYER' else 3 if x == 'BANKER' else 5 for x in last_10]
        
        # Verifica sequência Fibonacci
        for i in range(len(self.fibonacci_sequence) - 2):
            fib_seq = self.fibonacci_sequence[i:i+3]
            seq_str = ','.join(map(str, fib_seq))
            num_str = ','.join(map(str, numeric))
            
            if seq_str in num_str:
                next_val = self.fibonacci_sequence[i+3] if i+3 < len(self.fibonacci_sequence) else 3
                prediction = 'PLAYER' if next_val == 2 else 'BANKER' if next_val == 3 else 'TIE'
                return {
                    'prediction': prediction,
                    'confidence': 83 + (i * 2),
                    'reason': f'Fibonacci Dinâmico ({fib_seq})'
                }
        
        return {'prediction': None, 'confidence': 0, 'reason': ''}
    
    def _analyze_pressure_points(self) -> Dict:
        """Análise de pontos de pressão do sistema"""
        total = len(self.game_history)
        
        # Verifica pontos de pressão
        for point in self.pressure_points:
            if total % point == 0 and total >= point:
                # Determina a previsão baseada no desequilíbrio
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
        """Combina múltiplas previsões ponderadas"""
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
        
        # Seleciona a previsão com maior peso
        final_pred = max(pred_counts.items(), key=lambda x: x[1]['weight'])
        
        return {
            'prediction': final_pred[0],
            'confidence': final_pred[1]['confidence'] / final_pred[1]['weight'],
            'reason': ' | '.join(final_pred[1]['reasons'])
        }
    
    def _apply_bayesian_correction(self, prediction: Dict) -> Dict:
        """Aplica correção estatística bayesiana"""
        if len(self.game_history) < 50:
            return prediction
        
        last_100 = self.game_history[-100:]
        p_ratio = last_100.count('PLAYER') / len(last_100)
        b_ratio = last_100.count('BANKER') / len(last_100)
        
        # Correção para desequilíbrios
        if prediction['prediction'] == 'PLAYER' and p_ratio > 0.52:
            new_conf = prediction['confidence'] * 0.95
            return {
                **prediction,
                'confidence': max(75, new_conf),
                'reason': prediction['reason'] + ' | Correção Bayesiana (PLAYER super-representado)'
            }
        
        if prediction['prediction'] == 'BANKER' and b_ratio > 0.52:
            new_conf = prediction['confidence'] * 0.95
            return {
                **prediction,
                'confidence': max(75, new_conf),
                'reason': prediction['reason'] + ' | Correção Bayesiana (BANKER super-representado)'
            }
        
        return prediction
    
    def _smart_fallback(self) -> Dict:
        """Fallback inteligente quando nenhum padrão é detectado"""
        last_10 = self.game_history[-10:]
        p_count = last_10.count('PLAYER')
        b_count = last_10.count('BANKER')
        
        if p_count < 3:
            return {'prediction': 'PLAYER', 'confidence': 65, 'reason': 'Correção: PLAYER sub-representado'}
        if b_count < 3:
            return {'prediction': 'BANKER', 'confidence': 65, 'reason': 'Correção: BANKER sub-representado'}
        
        # Preferência estatística pelo BANKER (vantagem natural no Bac Bo)
        return {'prediction': 'BANKER', 'confidence': 58, 'reason': 'Vantagem estatística padrão'}
    
    def _update_stats(self, actual_result: str):
        """Atualiza estatísticas de acerto"""
        if self.last_prediction['prediction'] == actual_result:
            self.prediction_stats['wins'] += 1
        self.prediction_stats['total'] += 1
        self.last_predictions.append({
            'predicted': self.last_prediction['prediction'],
            'actual': actual_result,
            'confidence': self.last_prediction['confidence']
        })
    
    def get_stats(self) -> Dict:
        """Retorna estatísticas de desempenho"""
        if self.prediction_stats['total'] == 0:
            return {'win_rate': 0, 'total': 0}
        
        win_rate = (self.prediction_stats['wins'] / self.prediction_stats['total']) * 100
        return {
            'win_rate': win_rate,
            'total': self.prediction_stats['total'],
            'recent_predictions': list(self.last_predictions)
        }
    
    def reset(self):
        """Reinicia o sistema"""
        self.game_history = []
        self.prediction_stats = {'wins': 0, 'total': 0}
        self.last_predictions = deque(maxlen=20)
        if hasattr(self, 'last_prediction'):
            del self.last_prediction

# Exemplo de uso
if __name__ == "__main__":
    predictor = BacBoQuantumPredictor()
    
    # Simulação com dados (substitua por resultados reais)
    test_data = ['PLAYER', 'BANKER', 'PLAYER', 'PLAYER', 'BANKER', 
                 'BANKER', 'BANKER', 'PLAYER', 'TIE', 'BANKER',
                 'PLAYER', 'PLAYER', 'PLAYER', 'PLAYER', 'BANKER']
    
    for result in test_data:
        predictor.add_result(result)
    
    # Fazer previsão
    prediction = predictor.predict_next()
    print("\n🔮 Previsão Bac Bo Quantum:")
    print(f"Próxima aposta: {prediction['prediction']}")
    print(f"Confiança: {prediction['confidence']:.1f}%")
    print(f"Razão: {prediction['reason']}")
    
    # Ver estatísticas
    stats = predictor.get_stats()
    print(f"\n📊 Estatísticas: {stats['win_rate']:.1f}% de acerto ({stats['wins']}/{stats['total']})")
