<template>
  <div class="shell">
    <div class="image" id="a"></div>
    <div class="heading">
      <h1>Project Introduction</h1>
    </div>
    <div class="text">
      <h1>A powerful project</h1>
    </div>

    <div class="image" id="b"></div>
    <div class="heading">
      <h1>Team Style</h1>
    </div>
    <div class="text">
      <h1>A comprehensive team</h1>
    </div>

    <div class="image" id="c"></div>
    <div class="heading">
      <h1>Contact Us</h1>
    </div>
    <div class="text">
      <h1>Email:595927593@qq.com</h1>
    </div>

    <div class="image" id="d"></div>
    <div class="heading">
      <h1>Welcome to WatchDogs</h1>
    </div>
  </div>
</template>

<style>
* {
  padding: 0;
  margin: 0;
}

.shell {
  height: 100vh;
  overflow-x: hidden;
  perspective: 3px;
}

.shell div {
  position: relative;
  display: flex;
  justify-content: center;
  align-items: center;
  letter-spacing: 2px;
}

.image {
  transform: translateZ(-1px) scale(1.6);
  background-size: cover;
  height: 100vh;
  z-index: -1;
}

.text {
  height: 50vh;
  background-color: #fff;
}

.text h1 {
  color: #000;
}

.heading {
  z-index: -1;
  transform: translateY(-30vh) translateZ(1px);
  color: #fff;
  font-size: 30px;
}

#a {
  background-image: url("../assets/moon.jpg");
}

#b {
  background-image: url("../assets/mountain1.jpg");
}

#c {
  background-image: url("../assets/mountain3.jpg");
}

#d {
  background-image: url("../assets/mountain2.jpg");
}

</style>
