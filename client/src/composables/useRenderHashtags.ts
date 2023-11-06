import { Ref, computed } from 'vue'

const useRenderHashtags = (body: Ref<string>) => {
    return computed(() => {
        const words = body.value.split(' ');
        return words.filter(word => word.startsWith('#')).map(word => word.toLowerCase().replace('#', ''));
    })
}

export default useRenderHashtags