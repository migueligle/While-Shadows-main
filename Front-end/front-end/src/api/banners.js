import axios from 'axios'
const BASE_URL = 'http://127.0.0.1:8000/api'
export const fetchBanners = async (params) => {
  try {
    const token = localStorage.getItem('color')
    const config = {
      headers: {
        Authorization: `Bearer ${token}`
      },
      params: params
    }
    const response = await axios.get(`${BASE_URL}/banners/`, config)
    return response
  } catch (error) {
    this.$message.error('Error al realizar la petición', error)
    throw error
  }
}
export const fetchBannersBase = async (params) => {
  try {
    const response = await axios.get(`${BASE_URL}/banners-base/`)
    return response
  } catch (error) {
    this.$message.error('Error al realizar la petición', error)
    throw error
  }
}

export const fetchCreateBanner = async (dates) => {
  try {
    const token = localStorage.getItem('color')
    const config = {
      headers: {
        Authorization: `Bearer ${token}`
      }
    }
    const response = await axios.post(`${BASE_URL}/banners/`, dates, config)
    return response
  } catch (error) {
    this.$message.error('Error al realizar la petición', error)
    throw error
  }
}
export const fetchEditBanner = async (categorieId) => {
  try {
    const token = localStorage.getItem('color')
    const { id, ...data } = categorieId
    const config = {
      headers: {
        Authorization: `Bearer ${token}`
      }
    }
    const response = await axios.put(`${BASE_URL}/banners/${id}/`, data, config)
    return response.data
  } catch (error) {
    this.$message.error('Error al realizar la petición', error)
    throw error
  }
}
export const fetchDesactiveBanner = async (id) => {
  try {
    const token = localStorage.getItem('color')
    const productId = id
    const config = {
      headers: {
        Authorization: `Bearer ${token}`
      }
    }
    const response = await axios.put(`${BASE_URL}/banners/${productId}/deactivate_banner/`, {}, config)
    return response
  } catch (error) {
    this.$message.error('Error al realizar la petición', error)
    throw error
  }
}
