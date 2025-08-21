import axios from 'axios'
const BASE_URL = 'http://127.0.0.1:8000/api'

export const fetchCategories = async (params) => {
  try {
    const token = localStorage.getItem('color')
    const config = {
      headers: {
        Authorization: `Bearer ${token}`
      },
      params: params
    }
    const response = await axios.get(`${BASE_URL}/categories/`, config)
    return response
  } catch (error) {
    this.$message.error('Error al realizar la petición', error)
    throw error
  }
}
export const fetchCategoriesBase = async (params) => {
  try {
    const config = {
      params: params
    }
    const response = await axios.get(`${BASE_URL}/categories-base/`, config)
    return response
  } catch (error) {
    this.$message.error('Error al realizar la petición', error)
    throw error
  }
}
export const fetchDesactiveCategorie = async (id) => {
  try {
    const token = localStorage.getItem('color')
    const categorieId = id
    const config = {
      headers: {
        Authorization: `Bearer ${token}`
      }
    }
    const response = await axios.put(`${BASE_URL}/categories/${categorieId}/deactivate/`, {}, config)
    return response
  } catch (error) {
    this.$message.error('Error al realizar la petición', error)
    throw error
  }
}
export const fetchCreateCategorie = async (dates) => {
  try {
    const token = localStorage.getItem('color')
    const config = {
      headers: {
        Authorization: `Bearer ${token}`
      }
    }
    const response = await axios.post(`${BASE_URL}/categories/`, dates, config)
    return response
  } catch (error) {
    this.$message.error('Error al realizar la petición', error)
    throw error
  }
}
export const fetchEditCategorie = async (product) => {
  try {
    const token = localStorage.getItem('color')
    const { id, ...data } = product
    const config = {
      headers: {
        Authorization: `Bearer ${token}`
      }
    }
    const response = await axios.put(`${BASE_URL}/categories/${id}/edit/`, data, config)
    return response.data
  } catch (error) {
    this.$message.error('Error al realizar la petición', error)
    throw error
  }
}
