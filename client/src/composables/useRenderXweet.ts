import { RouterLink } from "vue-router"

const useRenderXweet = (text: string) => {
    const textArr = text.split(' ')
    return textArr.map(word => {
        return (
            word.startsWith('#') ?
            {
                type: RouterLink,
                to: `/trending?tag=${word.replace('#', '').toLowerCase()}`,
                text: word
            } :
            {
                type: 'span',
                text: word
            }
        )
    })
}

export default useRenderXweet