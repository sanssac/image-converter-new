export function fmtBytes(b) {
  if (!b || b < 0) return '0 B';
  const k = 1024, units = ['B','KB','MB','GB'];
  const i = Math.min(Math.floor(Math.log(b) / Math.log(k)), units.length - 1);
  return (b / Math.pow(k, i)).toFixed(1) + ' ' + units[i];
}
