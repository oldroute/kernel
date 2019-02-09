
let $backend = axios.create({
  baseURL: '/api',
  timeout: 5000,
  headers: {'Content-Type': 'application/json'}
})

$backend.$getBookRoot = () => {
  return $backend.get(`book/root/`).then(response => response.data)
}

$backend.$getPage = (pk) => {
  return $backend.get(`book/page/${pk}/`)
  .then(response => response.data)
}

$backend.$getTasks = (pk) => {
  return $backend.get(`book/page/${pk}/tasks/`)
  .then(response => response.data)
}

$backend.$getTask = (pk) => {
  return $backend.get(`book/task/${pk}/`)
  .then(response => response.data)
}

export default $backend
