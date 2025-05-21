export default function Square({ value, klik }) {
  return <div className='kotak' onClick={klik}>{value}</div>
}