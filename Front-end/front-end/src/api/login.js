import axios from 'axios'
import { jwtDecode } from 'jwt-decode'
const BASE_URL = 'http://127.0.0.1:8000/api'

export const fetchUserlogin = async (credentials) => {
  try {
    const response = await axios.post(`${BASE_URL}/login/`, credentials)
    return response.data
  } catch (error) {
    if (error.response) {
      this.$message.error('Error de respuesta del servidor:', error.response.data)
    } else if (error.request) {
      this.$message.error('No se recibió respuesta del servidor')
    } else {
      this.$message.error('Error:', error.message)
    }
    throw error
  }
}

export const fetchPostData = async (postId) => {
  try {
    const response = await axios.get(`${BASE_URL}/posts/${postId}`)
    return response.data
  } catch (error) {
    this.$message.error('Error al realizar la petición', error)
    throw error
  }
}

export const fetchUserData = async (params) => {
  try {
    const token = localStorage.getItem('color')
    const config = {
      headers: {
        Authorization: `Bearer ${token}`
      },
      params: params
    }
    const response = await axios.get(`${BASE_URL}/users/`, config)
    return response
  } catch (error) {
    this.$message.error('Error al realizar la petición', error)
    throw error
  }
}

export const CreateUser = async (dates) => {
  try {
    const response = await axios.post(`${BASE_URL}/register/`, dates)
    return response.data
  } catch (error) {
    if (error.response) {
      console.error('Error de respuesta del servidor:', error.response.data)
      console.error('Estado HTTP:', error.response.status)
    } else if (error.request) {
      console.error('No se recibió respuesta del servidor')
    } else {
      console.error('Error:', error.message)
    }
    throw error
  }
}

export const fetchDateUserData = async (params) => {
  try {
    const token = localStorage.getItem('color')
    let id = null
    if (token && token !== null) {
      const decodedToken = jwtDecode(token)
      id = decodedToken.id
    }
    id = Number(id)
    const config = {
      headers: {
        Authorization: `Bearer ${token}`
      },
      params: params
    }
    const response = await axios.get(`${BASE_URL}/users/${id}/`, config)
    return response
  } catch (error) {
    console.error('Error al recuperar datos', error)
    throw error
  }
}

export const fetchrecoverAccount = async (email) => {
  try {
    const response = await axios.post(`${BASE_URL}/users/recover-account/`, email)

    return response.data
  } catch (error) {
    if (error.response) {
      console.error('Error de respuesta del servidor:', error.response.data)
      console.error('Estado HTTP:', error.response.status)
    } else if (error.request) {
      console.error('No se recibió respuesta del servidor')
    } else {
      console.error('Error:', error.message)
    }
    throw error
  }
}

export const fetchDesactiveUser = async (id) => {
  try {
    const token = localStorage.getItem('color')
    let idToken = null
    if (token && token !== null) {
      const decodedToken = jwtDecode(token)
      idToken = decodedToken.id
    }
    const userId = id || idToken
    const config = {
      headers: {
        Authorization: `Bearer ${token}`
      }
    }
    const response = await axios.put(`${BASE_URL}/users/${userId}/desactive/`, {}, config)
    return response
  } catch (error) {
    console.error('Error al recuperar datos', error)
    throw error
  }
}
export const fetchChangePassword = async (id, dates) => {
  try {
    const token = localStorage.getItem('color')
    let idToken = null
    if (token && token !== null) {
      const decodedToken = jwtDecode(token)
      idToken = decodedToken.id
    }
    const userId = id || idToken
    const config = {
      headers: {
        Authorization: `Bearer ${token}`
      }
    }
    const response = await axios.put(`${BASE_URL}/users/${userId}/change_password/`, dates, config)
    return response
  } catch (error) {
    this.$message.error('Error al realizar la petición', error)
    throw error
  }
}

export const fetchUserEdit = async (dates) => {
  try {
    const token = localStorage.getItem('color')
    let idToken = null
    if (token && token !== null) {
      const decodedToken = jwtDecode(token)
      idToken = decodedToken.id
    }
    let id = dates.id || idToken
    id = Number(id)
    const config = {
      headers: {
        Authorization: `Bearer ${token}`
      }
    }
    const response = await axios.patch(`${BASE_URL}/users/${id}/edit/`, dates, config)
    return response
  } catch (error) {
    this.$message.error('Error al realizar la petición', error)
    throw error
  }
}

export const fetchUserEditDirection = async (dates, userId = null) => {
  try {
    const token = localStorage.getItem('color')
    let idToken = null
    if (token && token !== null) {
      const decodedToken = jwtDecode(token)
      idToken = decodedToken.id
    }
    let id = userId || idToken
    id = Number(id)
    const config = {
      headers: {
        Authorization: `Bearer ${token}`
      }
    }
    const response = await axios.put(`${BASE_URL}/users/${id}/edit_direction/`, dates, config)
    return response
  } catch (error) {
    this.$message.error('Error al realizar la petición', error)
    throw error
  }
}

export const fetchDateUserAddress = async (params) => {
  try {
    const token = localStorage.getItem('color')
    let id = null
    if (token && token !== null) {
      const decodedToken = jwtDecode(token)
      id = decodedToken.id
    }
    id = Number(id)
    const config = {
      headers: {
        Authorization: `Bearer ${token}`
      },
      params: params
    }
    const response = await axios.get(`${BASE_URL}/users/${id}/address/`, config)
    return response
  } catch (error) {
    this.$message.error('Error al realizar la petición', error)
    throw error
  }
}
export const ContactToAdmin = async (dates) => {
  try {
    const response = await axios.post(`${BASE_URL}/contact/`, dates)
    return response.data
  } catch (error) {
    if (error.response) {
      this.$message.error('Error de respuesta del servidor:', error.response.data)
      console.error('Estado:', error.response.status)
    } else if (error.request) {
      this.$message.error('No se recibió respuesta del servidor')
    } else {
      this.$message.error('Error:', error.message)
    }
    throw error
  }
}
