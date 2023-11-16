:root {
  --bg-color: #1e1e2e;
}

body {
  background: var(--bg-color);
  display: flex;
  align-items: center;
  flex-direction: column;
}

.container {
  font-family: sans-serif;
  font-weight: bold;
  
  position: relative;
  right: 0px;
  top: 0px;
  
  animation-fill-mode: forwards;
}

@keyframes move-n {
  from {right: 0px; top: 0px;}
  to {right: 200px; top: 200px;}
}

@keyframes move-e {
  from {right: 0px; top: 0px;}
  to {right: 140px; top: 70px;}
}

@keyframes move-i {
  from {right: 0px; top: 0px;}
  to {right: 100px; top: -20px;}
}

@keyframes move-l {
  from {right: 0px; top: 0px;}
  to {right: 60px; top: -145px;}
}


@keyframes pop-n {
  0% {right: 200px; top: 200px; color: #cdd6f4;}
  80% {right: 220px; color: #cdd6f4;}
  100% {right: 200px; color: #89b4fa;}
}

@keyframes pop-e {
  0% {right: 140px; top: 70px; color: #cdd6f4;}
  80% {right: 145px; color: #cdd6f4;}
  100% {right: 140px; top: 85px; color: #89b4fa;}
}

@keyframes pop-i {
  0% {right: 100px; top: -20px; color: #a6adc8;}
  80% {right: 95px; color: #a6adc8;}
  100% {right: 100px; top: -30px; color: #89b4fa;}
}

@keyframes pop-l {
  0% {right: 60px; color: #7f849c;}
  80% {right: 50px; color: #7f849c;}
  100% {right: 65px; color: #89b4fa;}
}

.n {
  color: #cdd6f4;
  animation-name: move-n, pop-n;
  animation-delay: 0s, 1s;
  animation-duration: 1s, 0.7s;

}

.e {
  color: #cdd6f4;
  animation-name: move-e, pop-e;
  animation-delay: 0s, 1.1s;
  animation-duration: 1s, 0.7s;
}

.i {
  color: #a6adc8;
  animation-name: move-i, pop-i;
  animation-delay: 0s, 1.2s;
  animation-duration: 1s, 0.7s;
}

.l {
  color: #7f849c;
  animation-name: move-l, pop-l;
  animation-delay: 0s, 1.1s;
  animation-duration: 1s, 0.7s;
}
