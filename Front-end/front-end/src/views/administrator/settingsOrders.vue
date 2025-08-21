<template>
  <div>
    <div>
      <el-page-header class="page-header" @back="goBack" title="Volver" content="Administración de Pedidos"></el-page-header>
    </div>
    <div class="content">
      <div>
        <el-col :sm="8" :md="6" :lg="4" :xl="2">
          <el-input
            placeholder="Email"
            v-model="email"
            clearable
            @input="debounceInput"
          ></el-input>
        </el-col>
        <el-col :sm="8" :md="6" :lg="4" :xl="2">
          <el-select
            v-model="is_paid"
            placeholder="Pagado"
            clearable
          >
            <el-option label="Pagado" value="true"></el-option>
            <el-option label="No pagado" value="false"></el-option>
          </el-select>
        </el-col>
        <el-col :sm="8" :md="6" :lg="8" :xl="4">
          <el-date-picker
          v-model="dateRange"
          type="daterange"
          start-placeholder="Fecha de inicio"
          end-placeholder="Fecha de fin"
          value-format="yyyy-MM-dd"
          range-separator="|"
          :clearable="true"
        ></el-date-picker>
        </el-col>
        <el-col :sm="8" :md="6" :lg="4" :xl="2">
          <el-select v-model="stat" placeholder="Estado" clearable filterable @change="dirtyFilter = true">
            <el-option :value="stateFilter.id" :key="stateFilter.id" :label="stateFilter.status" v-for="stateFilter in statusFilters "></el-option>
          </el-select>
        </el-col>
        <el-col :sm="8" :md="6" :lg="4" :xl="2">
          <el-button type="primary" icon="el-icon-search" @click="search">Buscar</el-button>
        </el-col>
      </div>
      <el-table ref="table" :data="orders" stripe style="width: 100%">
        <el-table-column
          v-for="column in columns"
          :key="column.label"
          :prop="column.prop"
          :label="column.label"
          :formatter="typeof column.formatter === 'function' ? column.formatter : null"
          :min-width="column.minWidth"
          :sortable="column.sortable"
        ></el-table-column>
        <el-table-column label="Pagado">
          <template v-slot="scope">
            <i
              :style="'border-radius: 10px; background-color: ' + (scope.row.is_paid === true ? 'rgb(0, 218, 0)' : 'rgb(255, 120, 120)') + '; color: white;'"
              :class="scope.row.is_paid === true ? 'el-icon-check' : 'el-icon-close'"
            ></i>
          </template>
        </el-table-column>
        <el-table-column style="min-width: 120px;" label="Operaciones" >
          <template v-slot="props">
            <el-button size="mini" @click="handleEditStatus(props.$index, props.row)"><i class="el-icon-edit-outline"></i></el-button>
            <el-button size="mini" type="danger" @click="handleCancel(props.$index, props.row)"><i class="el-icon-delete-solid"></i></el-button>
            <el-button size="mini" type="warning" @click="handleViewOrder(props.$index, props.row)"> <i class="el-icon-view"></i></el-button>
          </template>
        </el-table-column>
      </el-table>

      <el-pagination
        name="orderList"
        layout="total, sizes, prev, pager, next"
        :total="pagination.total"
        :page-sizes="pagination.pageSizes"
        :page-size="pagination.pageSize"
        :current-page="pagination.page"
        @size-change="handleSizeChange"
        @current-change="handleCurrentChange"
        background
      ></el-pagination>
    </div>
    <el-dialog
      title="Editar estado del Pedido"
      :visible="dialogEditStatusVisible"
      @before-close="cancelEditStatusForm"
      width="40%"
      :close-on-click-modal="false"
      :show-close="false"
    >
      <div>
        <el-form :model="editStatus" :rules="rules" ref="editStatusForm" label-width="120px" class="ruleForm">
          <el-form-item label="Estado del pedido:" prop="status">
            <el-select v-model="editStatus.status.id" placeholder="Estado" clearable filterable @change="dirtyFilter = true">
              <el-option :value="state.id" :key="state.id" :label="state.status" v-for="state in status"></el-option>
            </el-select>
          </el-form-item>
          <el-form-item>
            <el-button type="primary" @click="submitEditStatusForm('editStatusForm')">Guardar</el-button>
            <el-button @click="cancelEditStatusForm">Cancelar</el-button>
          </el-form-item>
        </el-form>
      </div>
    </el-dialog>
    <el-dialog
    title="Ver Productos"
    :visible="dialogViewOrderVisible"
    @before-close="handleBeforeCloseDialog"
    width="40%"
    :show-close="false"
  >
  <div>
    <el-card>
      <el-table ref="viewOrder" :data="viewOrder" stripe style="width: 100%">
        <el-table-column
          v-for="columnview of columnsView"
          :key="columnview.label"
          :prop="columnview.prop"
          :label="columnview.label"
          :formatter="typeof columnview.formatter === 'function' ? columnview.formatter : null"
          :min-width="columnview.minWidth"
          :sortable="columnview.sortable"
        ></el-table-column>
      </el-table>
    </el-card>
    <el-button @click="dialogViewOrderVisible = false">Volver</el-button>
  </div>
</el-dialog>
    <el-dialog
      title="Cancelar pedido"
      :visible="dialogCancelVisible"
      @before-close="dialogCancelVisible = false"
      width="40%"
      :close-on-click-modal="true"
      :show-close="false"
    >
      <div>
        <h3>¿Estás seguro de que quieres Cancelar el pedido?</h3>
        <el-button type="danger" @click="dialogCancelVisible = false, submitFormCancel('editStatusForm')">Cancelar</el-button>
        <el-button @click="dialogCancelVisible = false">Cancelar</el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>
import router from '@/router'
import { fetchOrders, fetchOrdersStatus, fetchEditOrder, fetchCancelOrder } from '@/api/orders'
import debounce from 'lodash/debounce'
import moment from 'moment'

export default {
  data () {
    return {
      status: [],
      rules: {
        status: [
          { required: true, message: 'El estado es requerido', trigger: 'change' }
        ]
      },
      viewOrder: [],
      columnsView: [
        {
          prop: 'mark',
          label: 'Marca',
          minWidth: '40px',
          sortable: true,
          formatter: row => row.mark
        },
        {
          prop: 'name',
          label: 'Productos',
          minWidth: '40px',
          sortable: true,
          formatter: row => row.name
        },
        {
          prop: 'quantity',
          label: 'Unidades',
          minWidth: '40px',
          sortable: true,
          formatter: row => row.quantity
        },
        {
          prop: 'price',
          label: 'Precio por Unidad',
          minWidth: '40px',
          sortable: true,
          formatter: row => row.price + ' ' + '€'
        },
        {
          prop: 'price',
          label: 'Precio Total',
          minWidth: '40px',
          sortable: true,
          formatter: row => row.total + ' ' + '€'
        }
      ],
      dateRange: [],
      statusFilters: [],
      dialogViewOrderVisible: false,
      is_paid: '',
      email: '',
      stat: '',
      state: '',
      editStatus: {
        status: {
          id: 0,
          status: ''
        }
      },
      stateFilter: '',
      orders: [],
      id: '',
      dialogEditStatusVisible: false,
      dialogCancelVisible: false,
      loading: false,
      columns: [
        {
          prop: 'id',
          label: 'ID',
          minWidth: '40px',
          sortable: true,
          formatter: row => row.id || ''
        },
        {
          prop: 'status',
          label: 'Estado',
          minWidth: '120px',
          sortable: true,
          formatter: row => row.status.status || ''
        },
        {
          prop: 'user_id',
          label: 'Id usuario',
          minWidth: '120px',
          sortable: true,
          formatter: row => row.user.id || ''
        },
        {
          prop: 'User',
          label: 'Usuario',
          minWidth: '120px',
          sortable: true,
          formatter: row => (row.user.last_name ? row.user.name + ' ' + row.user.last_name : row.user.name)
        },
        {
          prop: 'email',
          label: 'Email',
          minWidth: '120px',
          sortable: true,
          formatter: row => row.user.email || ''
        },
        {
          prop: 'created_at',
          label: 'Creado',
          minWidth: '80px',
          sortable: true,
          formatter: row => moment(row.created_at).format('DD/MM/YYYY HH:mm') || ''
        },
        {
          prop: 'total_amount',
          label: 'Total del pedido',
          minWidth: '120px',
          sortable: true,
          formatter: row => (Number(row.total_amount).toFixed(2).replace('.', ',') + ' €') || ''
        }
      ],
      pagination: {
        page: 1,
        total: 0,
        pageSizes: [10, 25, 50, 100],
        pageSize: 25
      }
    }
  },
  methods: {
    handleBeforeCloseDialog (action) {
      if (action) {
        this.dialogViewOrderVisible = false
      }
    },
    goBack () {
      router.push('/admin')
    },

    search () {
      this.fetchData()
    },
    debounceInput: debounce(function () {
      this.search()
    }, 500),
    fetchData (page) {
      this.loading = true
      const params = {
        page: page || this.pagination.page,
        page_size: this.pagination.pageSize
      }
      if (this.dateRange != null && this.dateRange !== '') {
        params.date_start = this.dateRange[0]
        params.date_end = this.dateRange[1]
      }
      if (this.email != null && this.email !== '') {
        params.email = this.email
      }
      if (this.is_paid != null && this.is_paid !== '') {
        params.is_paid = this.is_paid
      }
      if (this.stat != null && this.stat !== '') {
        params.status = this.stat
      }
      fetchOrders(params)
        .then(response => {
          this.orders = response.data.results
          this.pagination.total = response.data.count
          this.loading = false
        })
        .catch(error => {
          console.error('Error al recuperar datos', error)
          this.loading = false
        })
    },
    handleCurrentChange (newPage) {
      this.pagination.page = newPage
      this.fetchData()
    },
    handleViewOrder (index, row) {
      this.dialogViewOrderVisible = true
      this.viewOrder = [...row.items]
    },
    handleEditStatus (index, row) {
      this.dialogEditStatusVisible = true
      this.editStatus = { ...row }
    },
    handleSizeChange (pageSize) {
      this.pagination.pageSize = pageSize
      this.fetchData()
    },
    submitEditStatusForm (form) {
      if (this.$refs[form]) {
        this.$refs[form].validate(valid => {
          if (valid) {
            if (this.editStatus.status.id === '') { return this.$message.error('Por favor, completa correctamente el formulario.') }
            fetchEditOrder(this.editStatus)
              .then(() => {
                this.$message.success('Pedido editado correctamente')
                this.dialogEditStatusVisible = false
              })
              .catch(() => {
                this.$message.error('Error al editar el pedido')
              })
              .finally(() => {
                this.fetchData()
              })
          } else {
            this.$message.error('Por favor, completa correctamente el formulario.')
          }
        })
      } else {
        console.error('Referencia al formulario no encontrada:', form)
      }
    },
    cancelEditStatusForm () {
      this.dialogEditStatusVisible = false
    },
    submitFormCancel (form) {
      fetchCancelOrder(this.editStatus).then(() => {
        this.$message.success('Pedido Cancelado correctamente')
        this.dialogEditStatusVisible = false
      }).catch(() => {
        this.$message.error('Error al Cancelar el pedido')
      })
        .finally(() => {
          this.fetchData()
        })
    },
    handleCancel (index, row) {
      this.dialogCancelVisible = true
      this.editStatus = { ...row }
    },
    fetchOrdersStatus () {
      fetchOrdersStatus().then(response => {
        this.status = response.data
        this.statusFilters = response.data
      })
        .catch(error => {
          console.error('Error fetching orders status:', error)
        })
    },
    resetForm (formName) {
      this.$refs[formName].resetFields()
    }
  },

  mounted () {
    this.fetchData()
    this.fetchOrdersStatus()
  }
}
</script>

<style scoped>
.content {
  margin-top: 12%;
  margin-bottom: 12%;
  padding-left: 50px;
  padding-right: 50px;
}
.page-header {
  margin-left: 30px;
}
</style>
