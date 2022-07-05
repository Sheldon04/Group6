<template>
  <div class="a">
    <span style="--i:1">W</span>
    <span style="--i:2">A</span>
    <span style="--i:3">T</span>
    <span style="--i:4">C</span>
    <span style="--i:5">H</span>
    <span style="--i:6">D</span>
    <span style="--i:7">o</span>
    <span style="--i:8">g</span>
    <span style="--i:9">s</span>
  </div>
</template>

<script>
export default {
  name: 'banner'
}
</script>

<style scoped>
.a{
  position: relative;
  left: 400px;
  font: 900 70px '';
  color: #333;
  cursor: pointer;
}
.a span{
  transition: .5s;
  transition-delay: calc(var(--i)*.1s);
}
.a:hover span{
  color: #fff;
  text-shadow: 0 0 10px #fff,
  0 0 20px #fff,
  0 0 30px #fff,
  0 0 50px #fff,
  0 0 80px #fff;
}
</style>
