<template>
  <Suspense>
    <router-view :key="$route.path"></router-view>
  </Suspense>
</template>
