<script setup>
// import { ref, onMounted } from 'vue';
import UnityWebgl from 'unity-webgl';
import UnityVue from 'unity-webgl/vue';

// const unityContext = new UnityWebgl({
//   loaderUrl:
//     'https://static-huariot-com.oss-cn-hangzhou.aliyuncs.com/unity/test1/Build/OUT_BIM.loader.js',
//   dataUrl:
//     'https://static-huariot-com.oss-cn-hangzhou.aliyuncs.com/unity/test1/Build/OUT_BIM.data',
//   frameworkUrl:
//     'https://static-huariot-com.oss-cn-hangzhou.aliyuncs.com/unity/test1/Build/OUT_BIM.framework.js',
//   codeUrl:
//     'https://static-huariot-com.oss-cn-hangzhou.aliyuncs.com/unity/test1/Build/OUT_BIM.wasm',
// });

// const unityContext = new UnityWebgl({
//   loaderUrl:
//     'https://civildefense.fit.vutbr.cz/unity/Build/Build.loader.js',
//   dataUrl:
//     'https://civildefense.fit.vutbr.cz/unity/Build/Build.data',
//   frameworkUrl:
//     'https://civildefense.fit.vutbr.cz/unity/Build/Build.framework.js',
//   codeUrl:
//     'https://civildefense.fit.vutbr.cz/unity/Build/Build.wasm',
// });

const unityContext = new UnityWebgl({
  loaderUrl:
    'https://civildefense.fit.vutbr.cz/unity/Build/Build.loader.js',
  dataUrl:
    'https://civildefense.fit.vutbr.cz/unity/Build/Build.data.gz',
  frameworkUrl:
    'https://civildefense.fit.vutbr.cz/unity/Build/Build.framework.js.gz',
  codeUrl:
    'https://civildefense.fit.vutbr.cz/unity/Build/Build.wasm.gz',
});

unityContext.on('device', () => alert('click device ...'));
</script>

<template>
  <div style="width: 800px; height: 600px; border: 1px solid #f00">
    <UnityVue :unity="unityContext" tabindex="0" />
  </div>
</template>
