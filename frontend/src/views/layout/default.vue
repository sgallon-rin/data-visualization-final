<template>
  <v-layout>
    <v-navigation-drawer :clipped="clipped" v-model="drawer" disable-resize-watcher app>
      <v-list>
        <v-list-tile>
          <v-list-tile-action>
            <v-btn flat @click="$router.push('/')">Home</v-btn>
          </v-list-tile-action>
        </v-list-tile>
<!--        <v-list-tile>-->
<!--          <v-list-tile-action>-->
<!--            <v-btn flat @click="$router.push('/homework1')">Homework 1</v-btn>-->
<!--          </v-list-tile-action>-->
<!--        </v-list-tile>-->
<!--        <v-list-tile>-->
<!--          <v-list-tile-action>-->
<!--            <v-btn flat @click="$router.push('/homework2')">Homework 2</v-btn>-->
<!--          </v-list-tile-action>-->
<!--        </v-list-tile>-->
        <v-list-tile>
          <v-list-tile-action>
            <v-btn flat @click="$router.push('/final')">Final</v-btn>
          </v-list-tile-action>
        </v-list-tile>
      </v-list>
    </v-navigation-drawer>
    <v-toolbar fixed :clipped-left="clipped" color="blue" dark>
      <v-toolbar-title>
        <img @click="$router.push('/')" src="@/../public/img/logo.png" style="margin-top: 5px; cursor: grab"
             alt="logo.png" height="40px" width="40px">
      </v-toolbar-title>
      <v-toolbar-title>
        <!--HKUST VisLab Coding Challenge-->
        Data Visualization
      </v-toolbar-title>
      <v-spacer></v-spacer>
      <v-toolbar-items class="hidden-sm-and-down">
        <v-btn flat @click="$router.push('/')">Home</v-btn>
        <v-btn flat @click="$router.push('/homework1')">Homework 1</v-btn>
        <v-btn flat @click="$router.push('/homework2')">Homework 2</v-btn>
        <v-btn flat @click="$router.push('/final')">Final</v-btn>
      </v-toolbar-items>
      <v-toolbar-side-icon
          @click.stop="drawer = !drawer"
          class="hidden-md-and-up"
      >
      </v-toolbar-side-icon>
    </v-toolbar>
    <v-content>

      <v-container fluid fill-height>
        <v-layout justify-center>
          <router-view></router-view>
        </v-layout>
      </v-container>

    </v-content>
    <v-footer app dark color="blue">
      <span class="caption mx-3">&copy; 2021, Jialun Shen - Fudan University</span>
    </v-footer>
  </v-layout>
</template>

<script>
export default {
  name: "default",
  data: () => {
    return {
      drawer: false,
      clipped: false
    }
  }
}
</script>

<style scoped>
.v-content {
  padding-top: 56px !important;
}
</style>