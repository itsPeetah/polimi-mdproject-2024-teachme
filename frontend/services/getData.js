export default async function getData() {
    const res = await fetch('https://firebasestorage.googleapis.com/v0/b/teach-me-fc7c8.appspot.com/o/data.json?alt=media&token=218995c9-27e4-4a63-bddb-f21b8e56699a')
    if (!res.ok) {
        throw new Error('Failed to fetch data')
    }
    return res.json()
}