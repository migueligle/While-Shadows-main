import axios from 'axios'
const BASE_URL = 'http://127.0.0.1:8000/api'

export const fetchPaymentProcess = async (dates) => {
  try {
    const token = localStorage.getItem('color')
    const config = {
      headers: {
        Authorization: `Bearer ${token}`
      }
    }
    const response = await axios.post(`${BASE_URL}/payment-process/`, dates, config)
    return response
  } catch (error) {
    this.$message.error('Error al realizar la petición', error)
    throw error
  }
}
