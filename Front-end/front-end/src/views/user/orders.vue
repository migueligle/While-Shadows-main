 <template>
  <div>
    <div>
      <el-page-header class="page-header" @back="goBack" title="Volver" content="Administración de  Pedidos">
      </el-page-header>
    </div>
    <div class="content">
      <div>
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
        >
        </el-table-column>
        <el-table-column label="Pagado">
          <template v-slot="scope">
            <i
              :style="'border-radius: 10px; background-color: ' + (scope.row.is_paid === true ? 'rgb(0, 218, 0)' : 'rgb(255, 120, 120)') + '; color: white;'"
              :class="scope.row.is_paid === true ? 'el-icon-check' : 'el-icon-close'"
            ></i>
          </template>
        </el-table-column>
        <el-table-column style="min-width: 120px;"
      label="Operaciones" >
      <template v-slot="props"  >
        <i class="el-icon-view el-icon--custom-blue" @click="GoOrder(props.row)"></i>
        &nbsp;&nbsp;&nbsp;
        <i class="el-icon-back el-icon--custom-edit" @click="handleEdit(props.$index, props.row)"></i>
        &nbsp;&nbsp;&nbsp;
        <i class="el-icon-close   el-icon--custom-cancel" @click="handleDelete(props.$index, props.row)"></i>
      </template>
    </el-table-column>

      </el-table>

      <el-pagination
        name="UsersList"
        layout="total, sizes, prev, pager, next"
        :total="pagination.total"
        :page-sizes="pagination.pageSizes"
        :page-size="pagination.pageSize"
        :current-page="pagination.page"
        @current-change="handleCurrentChange"
        background
      >
      </el-pagination>
    </div>
    <el-dialog
        :title="`Devolución`"
        :visible="dialogEditVisible"
        @before-close="dialogEditVisible = false"
        width="40%"
        :close-on-click-modal="true"
      >
      <div>
        <h3>¿Estas seguro de que quieres devolver el pedido?</h3>
      <el-button type="warning" @click="dialogEditVisible = false,submitFormReturn('ruleForm')">confirmar</el-button>
      <el-button @click="dialogEditVisible = false">Cancelar</el-button>
      </div>
      </el-dialog>
      <el-dialog
        title="Cancelar pedido"
        :visible="dialogdeleteVisible"
        @before-close="dialogdeleteVisible = false"
        width="40%"
        :close-on-click-modal="true"
      >
      <div>
        <h3>¿Estás seguro de que quieres Cancelar el pedido?</h3>
        <el-button type="danger" @click="dialogdeleteVisible = false, submitFormCancel('ruleForm')">Confirmar</el-button>
        <el-button @click="dialogdeleteVisible = false">Cancelar</el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>
import router from '@/router'
import { fetchOrdersBase, fetchOrdersStatus, fetchReturnOrder, fetchCancelOrder } from '@/api/orders'
import moment from 'moment'
import { jwtDecode } from 'jwt-decode'

export default {
  name: 'ordersWhile',
  data () {
    return {
      dialogEditVisible: false,
      dialogdeleteVisible: false,
      orders: [],
      user_id: null,
      resetFields: [],
      is_paid: '',
      dateRange: [],
      stat: '',
      statusFilters: [],
      ruleForm: {},
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
  created () {
  },
  mounted () {
    if (localStorage.getItem('color')) {
      const decodedToken = jwtDecode(localStorage.getItem('color'))
      this.id = decodedToken.id
    }
    this.fetchData()
    this.fetchOrdersStatus()
  },
  methods: {
    submitFormReturn (form) {
      fetchReturnOrder(this.ruleForm).then(() => {
        this.$message.success('Solicitud de Devolución de pedido realizado correctamente')
        this.dialogdeleteVisible = false
      }).catch(() => {
        this.$message.error('El pedido no ha sido  enviado, por lo que no se puede devolver')
      })
        .finally(() => {
          this.fetchData()
        })
    },
    handleCancel (index, row) {
      this.dialogdeleteVisible = true
      this.ruleForm = { ...row }
    },
    resetForm (formName) {
      this.$refs[formName].resetFields()
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
    goBack () {
      router.push('/user')
    },
    GoOrder (order) {
      localStorage.setItem('order', JSON.stringify(order))
      this.$router.push({ name: 'orderShow', params: { order: order } })
    },
    search () {
      this.fetchData()
    },
    debounceInput: function () {
      if (this.debouncedInput) {
        clearTimeout(this.debouncedInput)
      }
      this.debouncedInput = setTimeout(() => {
        this.searchByEmail()
      }, 500)
    },
    fetchData (page) {
      this.loading = true
      const params = {
        page: page || this.pagination.page,
        page_size: this.pagination.pageSize,
        user_id: this.user_id
      }
      if (this.dateRange != null && this.dateRange !== '') {
        params.date_start = this.dateRange[0]
        params.date_end = this.dateRange[1]
      }
      if (this.is_paid != null && this.is_paid !== '') {
        params.is_paid = this.is_paid
      }
      if (this.stat != null && this.stat !== '') {
        params.status = this.stat
      }
      fetchOrdersBase(params)
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
    submitFormCancel (form) {
      fetchCancelOrder(this.ruleForm).then((response) => {
        this.$message.success('Pedido Cancelado correctamente')
        this.dialogEditStatusVisible = false
      }).catch(() => {
        this.$message.error('El pedido no se puede cancelar')
      })
        .finally(() => {
          this.fetchData()
        })
    },
    handleCurrentChange (newPage) {
      this.pagination.page = newPage
      this.fetchData()
    },
    handleEdit (index, row) {
      this.dialogEditVisible = true
      this.$set(this, 'ruleForm', { ...row })
    },
    handleDelete (index, row) {
      this.dialogdeleteVisible = true
      this.$set(this, 'ruleForm', { ...row })
    },
    searchByEmail () {
      if (this.email.trim() !== '') {
        this.fetchData()
      }
    },
    vieNewPassword () {
      if (this.showNewPassword === false) {
        this.showNewPassword = true
      } else {
        this.showNewPassword = false
      }
    }
  }
}
</script>

<style scoped>
.el-icon--custom-blue {
  color: #409EFF;
}
.el-icon--custom-blue:hover {
  color: #074f97;
}
.el-icon--custom-edit {
  color: #f7ba1f;
}
.el-icon--custom-edit:hover {
  color: #d6b108;
}
.el-icon--custom-cancel {
  color: #f82727;
}
.el-icon--custom-cancel:hover {
  color: #cb0b0b;
}
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
