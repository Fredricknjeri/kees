<template>
  <div class="heading">
    <h5>{{field.label}}</h5>
    <hr />
  </div>
</template>

<script>
export default {
  name: 'HeadingItem',
  props: {
    field: Object
  }
}
</script>