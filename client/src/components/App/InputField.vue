<script setup lang="ts">
import { ErrorObject } from '@vuelidate/core';

defineProps<{
    inputId: string,
    inputName: string,
    inputType: string,
    inputErrors?: ErrorObject[],
    modelValue?: string | null,
    labelText: string,
    icon: string
}>()
defineEmits<{
    (e: 'update:modelValue', value: string): void
}>()
</script>

<template>
    <section class="flex flex-col gap-1">
        <div :class="inputErrors && inputErrors.length > 0 ? 'border-red-600' : 'border-sky-600'"
            class="flex items-center w-48 px-2 py-1 border border-solid rounded-md">
            <div class="relative flex items-center justify-between w-full gap-1">
                <span v-if="inputName === 'username'" class="text-xs text-sky-600">@</span>
                <input 
                    :id="inputId" 
                    :name="inputName" 
                    :type="inputType" 
                    :value="modelValue"
                    @input="$emit('update:modelValue', ($event.target as HTMLInputElement).value)"
                    class="flex-1 min-w-0 text-white bg-transparent peer focus:outline-none" 
                    required>
                <font-awesome-icon 
                    :icon="icon" 
                    class="text-xs"
                    :class="inputErrors && inputErrors.length > 0 ? 'text-red-600' : 'text-sky-600'" />
                <label 
                    :for="inputId"
                    class="absolute text-xs transition-transform origin-top-left transform scale-100 translate-y-0 pointer-events-none text-slate-400 peer-focus:-translate-y-6 peer-focus:scale-90 peer-valid:-translate-y-6 peer-valid:scale-90"
                    :class="inputName === 'username' ? 'translate-x-4 peer-focus:-translate-x-[1px] peer-valid:-translate-x-[1px]' : 'translate-x-0'">
                    {{ labelText }}
                </label>
            </div>
        </div>
        <div class="w-48 text-xs text-red-400" v-for="error of inputErrors" :key="error.$uid">
            <span>{{ error.$message }}</span>
        </div>
    </section>
</template>