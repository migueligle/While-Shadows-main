import axios from 'axios'
const BASE_URL = 'http://127.0.0.1:8000/api'

export const fetchMarks = async (params) => {
  try {
    const token = localStorage.getItem('color')
    const config = {
      headers: {
        Authorization: `Bearer ${token}`
      },
      params: params
    }
    const response = await axios.get(`${BASE_URL}/marks/`, config)
    return response
  } catch (error) {
    this.$message.error('Error al realizar la petición', error)
    throw error
  }
}
export const fetchMarksBase = async (params) => {
  try {
    const config = {
      params: params
    }
    const response = await axios.get(`${BASE_URL}/marks-base/`, config)
    return response
  } catch (error) {
    this.$message.error('Error al realizar la petición', error)
    throw error
  }
}
export const fetchCreateMark = async (dates) => {
  try {
    const token = localStorage.getItem('color')
    const config = {
      headers: {
        Authorization: `Bearer ${token}`
      }
    }
    const response = await axios.post(`${BASE_URL}/marks/`, dates, config)
    return response
  } catch (error) {
    this.$message.error('Error al realizar la petición', error)
    throw error
  }
}
export const fetchEditMark = async (product) => {
  try {
    const token = localStorage.getItem('color')
    const { id, ...data } = product
    const config = {
      headers: {
        Authorization: `Bearer ${token}`
      }
    }
    const response = await axios.put(`${BASE_URL}/marks/${id}/`, data, config)
    return response.data
  } catch (error) {
    this.$message.error('Error al realizar la petición', error)
    throw error
  }
}
export const fetchDesactiveMark = async (id) => {
  try {
    const token = localStorage.getItem('color')
    const productId = id
    const config = {
      headers: {
        Authorization: `Bearer ${token}`
      }
    }
    const response = await axios.put(`${BASE_URL}/marks/${productId}/deactivate/`, {}, config)
    return response
  } catch (error) {
    this.$message.error('Error al realizar la petición', error)
    throw error
  }
}
