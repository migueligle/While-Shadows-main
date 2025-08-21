import axios from 'axios'
const BASE_URL = 'http://127.0.0.1:8000/api'

export const fetchProducts = async (params) => {
  try {
    const token = localStorage.getItem('color')
    const config = {
      headers: {
        Authorization: `Bearer ${token}`
      },
      params: params
    }
    const response = await axios.get(`${BASE_URL}/products/`, config)
    return response
  } catch (error) {
    this.$message.error('Error al realizar la petición', error)
    throw error
  }
}
export const fetchProductsBase = async (params) => {
  try {
    const response = await axios.get(`${BASE_URL}/products-base/`, { params: params })
    return response
  } catch (error) {
    this.$message.error('Error al realizar la petición', error)
    throw error
  }
}
export const fetchDateProductBase = async (params) => {
  try {
    const response = await axios.get(`${BASE_URL}/products-base/${params.productId}/`)
    return response.data
  } catch (error) {
    this.$message.error('Error al realizar la petición', error)
    throw error
  }
}
export const fetchCreateProduct = async (dates) => {
  try {
    const token = localStorage.getItem('color')
    const config = {
      headers: {
        Authorization: `Bearer ${token}`
      }
    }
    const response = await axios.post(`${BASE_URL}/products/`, dates, config)
    return response
  } catch (error) {
    this.$message.error('Error al realizar la petición', error)
    throw error
  }
}
export const fetchEditProduct = async (product) => {
  try {
    const token = localStorage.getItem('color')
    const { id, ...data } = product
    const config = {
      headers: {
        Authorization: `Bearer ${token}`
      }
    }
    const response = await axios.put(`${BASE_URL}/products/${id}/`, data, config)
    return response.data
  } catch (error) {
    this.$message.error('Error al realizar la petición', error)
    throw error
  }
}
export const fetchDesactiveProduct = async (id) => {
  try {
    const token = localStorage.getItem('color')
    const productId = id
    const config = {
      headers: {
        Authorization: `Bearer ${token}`
      }
    }
    const response = await axios.put(`${BASE_URL}/products/${productId}/deactivate_product/`, {}, config)
    return response
  } catch (error) {
    this.$message.error('Error al realizar la petición', error)
    throw error
  }
}
