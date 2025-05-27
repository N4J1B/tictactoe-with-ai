export function cekPemenang(isi) {
  const win = [
    [0, 1, 2], [3, 4, 5], [6, 7, 8],
    [0, 3, 6], [1, 4, 7], [2, 5, 8],
    [0, 4, 8], [2, 4, 6]
  ];
  for (let i = 0; i < win.length; i++) {
    const [a, b, c] = win[i];
    if (isi[a] && isi[a] === isi[b] && isi[a] === isi[c]) {
      return isi[a];
    }
  }
  if (!isi.includes(null)) {
    return 'Seri';
  }
  return null;
}

const evaluate = (isi, AI) => {
  const pemenang = cekPemenang(isi);
  if (pemenang === AI) {
    return 10;
  } else if (pemenang === (AI === 'X'? 'O' : 'X')) {
    return -10;
  } else if (!isi.includes(null)) {
    return 0;
  }
  return null;
}

function minimax(board, depth, isMaximizingPlayer, alpha, beta, AI) {
  const score = evaluate(board, AI);
  if (score !== null) {
    return score;    
  }

  let bestValue;

  if (isMaximizingPlayer) {
    bestValue = -Infinity;
    for (let i = 0; i < board.length; i++) {
      if (board[i] === null) {
        board[i] = AI;
        const value = minimax(board, depth + 1, false, alpha, beta, AI);
        board[i] = null;
        bestValue = Math.max(bestValue, value);
        alpha = Math.max(alpha, bestValue);
        if (beta <= alpha) {
          break; // Alpha-Beta Pruning
        }
      }
    }
    return bestValue;
  } else {
    bestValue = Infinity;
    for (let i = 0; i < board.length; i++) {
      if (board[i] === null) {
        board[i] = (AI == 'X' ? 'O' : 'X');
        const value = minimax(board, depth + 1, true, alpha, beta, AI);
        board[i] = null; 
        bestValue = Math.min(bestValue, value);
        beta = Math.min(beta, bestValue);
        if (beta <= alpha) {
          break; // Alpha-Beta Pruning
        }
      }
    }
    return bestValue;
  }
};

export const findBestMove = (currentBoard, AI) => {
  let bestValue = -Infinity;
  let bestMove = -1;

  for (let i = 0; i < currentBoard.length; i++) {
    if (currentBoard[i] === null) {
      currentBoard[i] = AI
      const moveValue = minimax(currentBoard, 0, false, -Infinity, Infinity, AI);
      currentBoard[i] = null;

      if (moveValue > bestValue) {
        bestValue = moveValue;
        bestMove = i;
      }
    }
  }
  return bestMove;
};