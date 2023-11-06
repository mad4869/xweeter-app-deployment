const useTimestamp = (date?: string) => {
    if (!date) {
        return ''
    }

    const currentDate = new Date()
    const pastDate = new Date(date)
    const deltaDate = currentDate.getTime() - pastDate.getTime()

    const seconds = Math.floor(deltaDate / 1000)
    const minutes = Math.floor(seconds / 60)
    const hours = Math.floor(minutes / 60)
    const days = Math.floor(hours / 24)
    const months = Math.floor(days / 30)
    const years = Math.floor(months / 12)

    switch(true) {
        case years > 0:
            return `${years} year${years !== 1 ? 's' : ''} ago`
        case months > 0:
            return `${months} month${months !== 1 ? 's' : ''} ago`
        case days > 0:
            return `${days} day${days !== 1 ? 's' : ''} ago`
        case hours > 0:
            return `${hours} hour${hours !== 1 ? 's' : ''} ago`
        case minutes > 0:
            return `${minutes} minute${minutes !== 1 ? 's' : ''} ago`
        default:
            return `${seconds} second${seconds !== 1 ? 's' : ''} ago`
    }
}

export default useTimestamp