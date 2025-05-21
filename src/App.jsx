import { useEffect, useState } from 'react';
import './App.css';
import Square from './kotak.jsx'

export default function App () {
const [histori, setHistori] = useState([Array(9).fill(null)])
const [move, setMove] = useState(0)
const [isi, setIsi] = useState(Array(9).fill(null))
const giliranX = move%2 === 0 //true

const handleClick = (i) => {
    if(isi[i] || cekPemenang(isi)) return
    const isiBaru = isi.slice()
    const historiBaru = [...histori, isiBaru]
    isiBaru[i] = giliranX ? 'X' : 'O'
    setHistori(historiBaru)
    setIsi(isiBaru)
    setMove(historiBaru.length - 1)
  }
  
  const undo = () => {
    if(histori.length === 1) return alert("belum mulai")
    setIsi(histori[move - 1])
    setHistori(histori.slice(0, histori.length -1))
    setMove(move -1)
}

const reset = () => {
  setIsi(histori[0])
  setMove(0)
  setHistori(histori.slice(0,1))
}

  useEffect(() => {
    console.log(histori)
    console.log(isi)
    console.log('move ' + move)
  })

  const pemenang = cekPemenang(isi)
  let hasil = "Giliran : " + (giliranX ? 'X' : 'O')
  if (pemenang) {
    hasil = "Pemenang : "+ pemenang
  }
  return (
    <>
    <div className='status'>
      {hasil}
      <button className="btn" onClick={undo}>Undo</button>
      <button className="btn" onClick={reset}>Reset</button>
    </div>
    <div className="App">
      <Square value={isi[0]} klik={() => handleClick(0)}/>
      <Square value={isi[1]} klik={() => handleClick(1)}/>
      <Square value={isi[2]} klik={() => handleClick(2)}/>
      <Square value={isi[3]} klik={() => handleClick(3)}/>
      <Square value={isi[4]} klik={() => handleClick(4)}/>
      <Square value={isi[5]} klik={() => handleClick(5)}/>
      <Square value={isi[6]} klik={() => handleClick(6)}/>
      <Square value={isi[7]} klik={() => handleClick(7)}/>
      <Square value={isi[8]} klik={() => handleClick(8)}/>
    </div>
    </>
  );
}

function cekPemenang(isi){
  const win = [
    [0, 1, 2],
    [3, 4, 5],
    [6, 7, 8],
    [0, 3, 6],
    [1, 4, 7],
    [2, 5, 8],
    [0, 4, 8],
    [2, 4, 6]
  ]
for (let i = 0; i < win.length; i++) {
  const [a, b, c] = win[i]
  if (isi[a] && isi[a] === isi[b] && isi[a] === isi[c] ){
    return isi[a]
  }
}
return false
}