---
source: "website"
content_type: "blogs_resources"
url: "https://gearboxgo.com/articles/web-application-development/nuxt-form-validation-with-precognition-and-zod"
title: "Nuxt Form Validation with Precognition and Zod"
domain: "gearboxgo.com"
path: "/articles/web-application-development/nuxt-form-validation-with-precognition-and-zod"
scraped_time: "2025-10-05T01:39:48.789201"
url_depth: 3
word_count: 700
client_name: "gearbox-solutions"
---

# Nuxt Form Validation with Precognition and Zod

## The Struggle

Validating form data is a key part of receiving user input. Validation can take place on both the client, before data is submitted, and on the server, after the input has been received.

Validating data client side before it is submitted can provide a very nice user experience, but the most important validation is server-side, before processing the received data. Client-side validation can be bypassed, and so should never be trusted. With server-side validation, you can be sure that the validation has processed successfully.

[Nuxt Precognition](https://github.com/gearbox-solutions/nuxt-precognition) provides a straightforward way to use your server-side validation on the client before submitting your form.

This leads to a common struggle with validation, where developers end up wanting to perform validation on both the client and the server. Client-side validation for UX, and server-side validation for security. Keeping both of these validations in-sync can be a bit of a pain. As an additional challenge, some validation can only be performed server-side, such as making sure that an email address is unique.

## The Solution

We've released [Nuxt Precognition](https://github.com/gearbox-solutions/nuxt-precognition) as a Nuxt module to allow you to configure your validation server-side, while using that same configuration to do (what appears to be) client-side validation before users have submitted their form data.

Normally this validation process would require creating additional Nuxt server API routes which would be responsible for performing validation before form data are submitted. Nuxt Precognition provides the tools to allow for as little as a single field to be validated at a time, without the need to create additional server endpoints or validation logic.

Our focus on this is to provide a very simple developer interface, to allow for creating validation with as few lines of code and configuration options as possible. This module is inspired by [Laravel Precognition](https://laravel.com/docs/11.x/precognition), and strives to bring similar hybrid client/server validation integration to the Nuxt ecosystem.

### Client-Side

Nuxt Precognition provides a `useForm` and `usePrecognitionForm` composable for use in your Vue components. These composables provide a great DX for managing form state and submittion. The two composables are very similar, but the `usePrecognitionForm` also provides the "precognition magic"

```typescript
<script setup lang="ts">
const form = usePrecognitionForm('post', '/api/todo-precog', {
  name: '',
  age: null,
})

const submitForm = async () => {
  await form.submit({
    onSuccess: (response) => {
      // do something with the response

    },
  })
}
</script>
```

Validation can be triggered by calling `form.validate('myFieldName')`. Putting this on an @change event listener on an input element is a good way to trigger this. Errors are placed in `form.errors` as an array of failed validation errors.

```html
<input
  id="age"
  v-model="model"
  name="age"
  class="rounded-md px-2 py-1"
  @change="form.validate('age')"
>
<div
  v-for="error in form.errors.age"
  :key="error"
  class="text-red-500"
>
  {{ error }}
</div>
```

### Server-Side

The Nuxt Precognition module provides a `definePrecognitionEventHandler` utility which replaces your regular `defineEventHandler` and takes [Zod validation schemas](https://zod.dev/) to perform the validation of your data before your event handler actually runs. Vue `usePrecognitionForm` and `useForm` composables provide formatted validation data which can be triggered with a simple `@change` event on an input field.

As an example, your server-side event handler would change from:

```javascript
export default defineEventHandler(async (event) => {
// do stuff here
```

to:

```javascript
const formValidationSchema = z.object({
  name: z.string().trim().min(1, 'Name is required'),
  age: z.number().min(18, 'Must be at least 18 years old'),
})

export default definePrecognitionEventHandler(formValidationSchema, async (event) => {
// do regular eventHandler stuff here
// this doesn't run when performing precognition validation!
```

This `definePrecognitionEventHandler` intercepts "precognition" requests for validation and stops your handler from running, meaning that the validation requests just do the validation and then stop. This makes running the just-validation requests very efficient.

## Try it out!

Our goal with this package is to provide as simple of a DX as possible for implementing form validation and getting a result back on the server. We're early in the development process of this and are interested in hearing feedback about the implementation. We'd love for you to try it out!

Try the [demo on Stackblitz](https://stackblitz.com/github/gearbox-solutions/nuxt-precognition?file=playground%2Fpages%2Fregister-precog.vue).

The module can be installed with the following command:

```
npx nuxi module add @gearbox-solutions/nuxt-precognition
```

Documentation and an example implementation are [available on GitHub](https://github.com/gearbox-solutions/nuxt-precognition).