from flask import Flask, request, jsonify
from flask_cors import CORS
import pickle
import numpy as np

class Board:
    def __init__(self):
        """
        Menginisialisasi objek Board untuk permainan Tic-Tac-Toe.
        Board direpresentasikan sebagai array NumPy 1D berukuran 9.
        """
        self.board = np.zeros(9, dtype=int)  # Board 1D: 0=kosong, 1=Pemain 1, -1=Pemain -1
        self.player = 1  # Pemain saat ini: 1 atau -1
        self.winner = 0  # Pemenang: 0=belum ada, 1=Pemain 1, -1=Pemain -1, 2=Seri
        self.history = []  # Riwayat langkah-langkah board

    def reset(self):
        """
        Mengatur ulang board ke keadaan awal untuk permainan baru.
        """
        self.board = np.zeros(9, dtype=int)
        self.player = 1
        self.winner = 0
        self.history = []

    def available_moves(self):
        """
        Mengembalikan daftar indeks langkah yang tersedia (sel yang kosong).
        """
        return [i for i, x in enumerate(self.board) if x == 0]

    def make_move(self, index):
        """
        Melakukan langkah pada indeks yang diberikan.
        Mengembalikan True jika langkah valid, False jika tidak.
        """
        if 0 <= index < 9 and self.board[index] == 0:
            self.board[index] = self.player
            self.history.append(tuple(self.board)) # Menyimpan keadaan board ke riwayat
            self.player *= -1
            self.check_winner()
            return True
        return False

    def check_winner(self):
        """
        Memeriksa apakah ada pemenang atau permainan seri.
        Memperbarui atribut self.winner.
        """
        winning_combinations = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8], # Rows
            [0, 3, 6], [1, 4, 7], [2, 5, 8], # Columns
            [0, 4, 8], [2, 4, 6]             # Diagonals
        ]

        for combo in winning_combinations:
            s = self.board[combo[0]] + self.board[combo[1]] + self.board[combo[2]]
            if abs(s) == 3:
                self.winner = s // 3
                return

        if len(self.available_moves()) == 0 and self.winner == 0:
            self.winner = 2

    def get_board_state(self):
        """
        Mengembalikan keadaan board saat ini sebagai tuple (immutable).
        """
        return tuple(self.board)

    def get_player_turn(self):
        """
        Mengembalikan giliran pemain saat ini (1 atau -1).
        """
        return self.player

class Agent: # Nama kelas diubah menjadi QAgent untuk membedakan
    def __init__(self, name, player_id, epsilon_start=1.0, epsilon_end=0.01, epsilon_decay_rate=0.9999, alpha=0.9, gamma=0.9):
        """
        Menginisialisasi objek QAgent untuk bermain Tic-Tac-Toe menggunakan Tabular Q-Learning.
        
        Args:
            name (str): Nama agen.
            player_id (int): ID pemain yang diwakili agen (1 atau -1).
            epsilon_start (float): Nilai epsilon awal untuk eksplorasi.
            epsilon_end (float): Nilai epsilon minimum.
            epsilon_decay_rate (float): Tingkat peluruhan epsilon per episode.
            alpha (float): Tingkat pembelajaran (learning rate).
            gamma (float): Faktor diskon untuk nilai masa depan.
        """
        self.name = name
        self.player_id = player_id
        self.epsilon = epsilon_start
        self.epsilon_start = epsilon_start
        self.epsilon_end = epsilon_end
        self.epsilon_decay_rate = epsilon_decay_rate
        self.alpha = alpha
        self.gamma = gamma
        self.q_table = {}  # Kamus untuk menyimpan Q-value: {state_tuple: {action_index: Q_value}}
        self.history_state_actions = [] # Riwayat (state, action) yang diambil agen dalam satu episode

    def get_q_value(self, state, action):
        """Mengambil Q-value untuk state-action pair."""
        if state not in self.q_table:
            self.q_table[state] = {i: 0.0 for i in range(9)} # Inisialisasi Q-value untuk semua aksi menjadi 0.0
        return self.q_table[state].get(action, 0.0) # Mengembalikan 0.0 jika aksi belum ada

    def choose_action(self, board_obj):
        """
        Memilih langkah berdasarkan strategi epsilon-greedy menggunakan Q-table.
        
        Args:
            board_obj (Board): Objek Board permainan saat ini.
            
        Returns:
            int: Indeks langkah yang dipilih.
        """
        current_state = board_obj.get_board_state()
        available_moves = board_obj.available_moves()
        
        if not available_moves:
            return None

        # Eksplorasi: Pilih langkah acak dengan probabilitas epsilon
        if np.random.uniform(0, 1) <= self.epsilon:
            action = np.random.choice(available_moves)
        else:
            # Eksploitasi: Pilih langkah dengan nilai Q-value tertinggi
            q_values_for_moves = {}
            for move_index in available_moves:
                q_values_for_moves[move_index] = self.get_q_value(current_state, move_index)
            
            # Cari Q-value maksimum
            max_q_value = -float('inf')
            for q_val in q_values_for_moves.values():
                if q_val > max_q_value:
                    max_q_value = q_val
            
            # Kumpulkan semua aksi yang memiliki Q-value maksimum
            best_actions = [move for move, q_val in q_values_for_moves.items() if q_val == max_q_value]
            
            # Pilih satu aksi secara acak dari yang terbaik (untuk tie-breaking)
            action = np.random.choice(best_actions)
        
        return action

    def add_state_action(self, state, action):
        """
        Menambahkan pasangan (state, action) yang diambil agen ke riwayat.
        """
        self.history_state_actions.append((state, action))

    def learn(self, board_obj):
        """
        Memperbarui nilai Q-value berdasarkan hasil permainan (reward) menggunakan Q-learning.
        """
        reward = 0
        if board_obj.winner == self.player_id:
            reward = 1      # Agen menang
        elif board_obj.winner == -self.player_id:
            reward = -1     # Agen kalah
        elif board_obj.winner == 2:
            reward = 0.5    # Permainan seri

        # Iterasi mundur melalui riwayat (state, action)
        # Dengan Q-Learning, kita memperbarui Q(S,A) berdasarkan Q(S',A')
        # S_t+1 adalah state setelah aksi A_t, A_t+1 adalah aksi optimal di S_t+1
        
        # Q-learning off-policy: Q(S,A) <- Q(S,A) + alpha * [R + gamma * max_a' Q(S',a') - Q(S,A)]
        
        # Jika ini adalah state terminal, reward langsung diberikan, tidak ada Q(S',A')
        
        # Dapatkan state_action terakhir dari history
        # Perhatikan bahwa history_state_actions sudah dalam urutan kronologis.
        # Kita akan iterasi dari yang terakhir (state sebelum terminal) ke yang pertama.

        # Nilai Q max untuk state terminal adalah 0 (karena tidak ada aksi lagi)
        next_q_max = 0.0

        # Iterasi mundur melalui riwayat (state, action)
        for state, action in reversed(self.history_state_actions):
            # Pastikan state ada di q_table
            if state not in self.q_table:
                self.q_table[state] = {i: 0.0 for i in range(9)}

            # Hitung TD Target
            if next_q_max is None: # Ini hanya akan terjadi untuk state terminal
                td_target = reward
            else:
                td_target = reward + self.gamma * next_q_max
            
            # Hitung TD Error
            td_error = td_target - self.get_q_value(state, action)
            
            # Perbarui Q-value
            self.q_table[state][action] = self.get_q_value(state, action) + self.alpha * td_error
            
            # Untuk iterasi berikutnya, next_q_max adalah Q-value dari state saat ini yang baru diperbarui
            # Namun, ini adalah Q-value dari state-action PAIR yang baru saja diambil.
            # Q-learning menggunakan max_a' Q(S',a')
            # Jadi, next_q_max untuk langkah sebelumnya adalah Q-value tertinggi dari state 'state' saat ini.
            
            # Jika state saat ini bukan state awal permainan dan bukan state terminal
            # Kita perlu mencari max Q(S,a) dari state 'state' untuk semua aksi yang mungkin.
            # Ini adalah estimasi terbaik dari nilai state 'state' itu sendiri.
            next_q_max = max(self.q_table[state].values()) # Q-value optimal dari state 'state'

            # Set reward untuk langkah selanjutnya menjadi 0 (reward hanya di akhir episode)
            reward = 0 
            
        self.history_state_actions = [] # Mengosongkan riwayat setelah pembelajaran

    def update_epsilon(self, episode):
        """
        Memperbarui nilai epsilon (untuk eksplorasi) berdasarkan episode.
        """
        self.epsilon = max(self.epsilon_end, self.epsilon_start * (self.epsilon_decay_rate ** episode))

# --- Akhir Re-Definisi Kelas Board dan Agent ---

app = Flask(__name__)
CORS(app)

# --- Memuat Model yang Sudah Terlatih ---
MODEL_FILENAME = 'tictactoe_agent_x.pkl'
MODEL_FILENAME2 = 'tictactoe_agent_o.pkl'
ai_agent1 = None
ai_agent2 = None

try:
    with open(MODEL_FILENAME, 'rb') as f:
        ai_agent1 = pickle.load(f)
    print(f"AI Agent berhasil dimuat dari '{MODEL_FILENAME}'.")
except FileNotFoundError:
    print(f"Error: File model '{MODEL_FILENAME}' tidak ditemukan. Pastikan model telah dilatih dan disimpan.")
except Exception as e:
    print(f"Error saat memuat model: {e}")

try:
    with open(MODEL_FILENAME2, 'rb') as f:
        ai_agent2 = pickle.load(f)
    print(f"AI Agent berhasil dimuat dari '{MODEL_FILENAME2}'.")
except FileNotFoundError:
    print(f"Error: File model '{MODEL_FILENAME2}' tidak ditemukan. Pastikan model telah dilatih dan disimpan.")
except Exception as e:
    print(f"Error saat memuat model: {e}")

# --- Endpoint API untuk Prediksi Langkah ---
@app.route('/predict_move', methods=['POST'])
def predict_move():
    if (ai_agent1 is None) or (ai_agent2 is None):
        return jsonify({"error": "AI Agent belum dimuat. Mohon latih model terlebih dahulu."}), 500

    data = request.json
    current_board_flat = data.get('board') # Diharapkan list 1D berisi 9 elemen
    player_turn = data.get('player_turn') # 1 atau -1 (pemain yang sedang giliran)

    # Validasi input
    if not isinstance(current_board_flat, list) or len(current_board_flat) != 9 or \
       not all(isinstance(x, int) and x in [-1, 0, 1] for x in current_board_flat):
        return jsonify({"error": "Format board tidak valid. Diharapkan list 1D dengan 9 integer (0, 1, atau -1)."}), 400

    if player_turn not in [1, -1]:
        return jsonify({"error": "player_turn tidak valid. Diharapkan 1 atau -1."}), 400

    # Konversi list 1D ke numpy array 1D
    board_array = np.array(current_board_flat, dtype=int)

    # Buat objek Board sementara untuk melakukan prediksi
    temp_board_obj = Board()
    temp_board_obj.board = board_array
    temp_board_obj.player = player_turn # Set giliran pemain sesuai request

    # Pastikan AI bermain sebagai player_turn yang diminta dalam request ini
    if player_turn == 1:
        ai_agent1.player_id = player_turn
        move_index = ai_agent1.choose_action(temp_board_obj) # Akan mengembalikan indeks 0-8
    elif player_turn == -1:
        ai_agent2.player_id = player_turn
        move_index = ai_agent2.choose_action(temp_board_obj) # Akan mengembalikan indeks 0-8
        
    # Dapatkan saran langkah dari agen AI

    if move_index is not None:
        # Konversi indeks 1D ke koordinat (row, col) untuk output yang lebih mudah dipahami
        row = move_index // 3
        col = move_index % 3
        return jsonify({"move": {"index": int(move_index), "row": int(row), "col": int(col)}})
    else:
        return jsonify({"move": None, "message": "Tidak ada langkah yang tersedia atau permainan sudah berakhir."})


@app.route('/qtable1', methods=['GET'])
def get_qtable1():
    json_output_data = {}
    limit = 50
    count = 0

    for state_tuple, actions_q_values in ai_agent1.q_table.items():
        if limit is not None and count >= limit:
            break
        state_key_str = str(tuple(x.item() for x in state_tuple))
        json_output_data[state_key_str] = actions_q_values
        count += 1
    return jsonify(json_output_data)

@app.route('/qtable2', methods=['GET'])
def get_qtable2():
    json_output_data = {}
    limit = 50
    count = 0

    for state_tuple, actions_q_values in ai_agent2.q_table.items():
        if limit is not None and count >= limit:
            break
        state_key_str = str(tuple(x.item() for x in state_tuple))
        json_output_data[state_key_str] = actions_q_values
        count += 1
    return jsonify(json_output_data)



# --- Endpoint Health Check ---
@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy", "model_loaded": [ai_agent1 is not None, ai_agent2 is not None]})

# --- Menjalankan Aplikasi Flask ---
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=82)