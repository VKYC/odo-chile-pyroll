# -*- coding: utf-8 -*-
##############################################################################
# Chilean Payroll
# Odoo / OpenERP, Open Source Management Solution
# By Blanco Mart�n & Asociados - Nelson Ram�rez S�nchez (http://blancomartin.cl).
#
# Derivative from Odoo / OpenERP / Tiny SPRL
#
# WARNING: This program as such is intended to be used by professional
# programmers who take the whole responsability of assessing all potential
# consequences resulting from its eventual inadequacies and bugs
# End users who are looking for a ready-to-use solution with commercial
# garantees and support are strongly adviced to contract a Free Software
# Service Company
#
# This program is Free Software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.
#
##############################################################################

import datetime
import time
from openerp.osv import osv, fields 
from openerp.report import report_sxw

class report_hr_salary_employee_bymonth(report_sxw.rml_parse):

    def __init__(self, cr, uid, name, context):
        super(report_hr_salary_employee_bymonth, self).__init__(cr, uid, name, context=context)

        self.localcontext.update({
            'time': time,
            'get_employee': self.get_employee,
            'get_employee2': self.get_employee2,
            'get_analytic': self.get_analytic,


            
            
        })

        self.context = context
        self.mnths = []
        self.mnths_total = []
        self.total = 0.0

    def get_worked_days(self, form, emp_id, emp_salary, mes, ano):

        self.cr.execute("select number_of_days from hr_payslip_worked_days as p  \
                           left join hr_payslip as r on r.id = p.payslip_id   \
                           where r.employee_id = %s  and (to_char(date_to,'mm')= %s) \
                             and (to_char(date_to,'yyyy')= %s) and p.code ='WORK100'  \
                            group by number_of_days",(emp_id, mes, ano,)) \
        
        
        max = self.cr.fetchone()
        
        if max is None:
        	emp_salary.append(0.00)
        else:
        	emp_salary.append(max[0])

        return emp_salary


    def get_employe_basic_info(self, emp_salary, cod_id, mes, ano):

        self.cr.execute("select sum(pl.total) \
                             from hr_payslip_line as pl \
                             left join hr_payslip as p on pl.slip_id = p.id \
                             left join hr_employee as emp on emp.id = p.employee_id \
                             left join resource_resource as r on r.id = emp.resource_id  \
                            where p.state = 'done' and (pl.code like %s) and (to_char(date_to,'mm')=%s) and (to_char(date_to,'yyyy')=%s) \
                            group by r.name, p.date_to",(cod_id, mes, ano,))  
        
        
        max = self.cr.fetchone()
        
        if max is None:
        	emp_salary.append(0.00)
        else:
        	emp_salary.append(max[0])

        return emp_salary

    def get_analytic(self, form):
        emp_salary = []
        salary_list = []
        last_year = form['end_date'][0:4]
        last_month = form['end_date'][5:7]
        cont = 0



        self.cr.execute("select sum(pl.total), w.name \
                             from hr_payslip_line as pl \
                             left join hr_payslip as p on pl.slip_id = p.id \
                             left join hr_employee as emp on emp.id = p.employee_id   \
                             left join hr_contract as r on r.id = p.contract_id  \
                             left join account_analytic_account as w on w.id = r.analytic_account_id  \
                            where p.state = 'done'  and (to_char(date_to,'mm')=%s)   \
                            and (to_char(date_to,'yyyy')=%s)  \
                            group by  w.name order by name",( last_month, last_year,))  
    
        id_data = self.cr.fetchall()
        if id_data is None:
            emp_salary.append(0.00)
            emp_salary.append(0.00)

        else:
            for index in id_data:
                emp_salary.append(id_data[cont][0])
                emp_salary.append(id_data[cont][1])

                cont = cont + 1
                salary_list.append(emp_salary)
                
                emp_salary = []
        
        return salary_list





    def get_salary(self, emp_id, emp_salary, cod_id, mes, ano):

        self.cr.execute("select sum(pl.total) \
                             from hr_payslip_line as pl \
                             left join hr_payslip as p on pl.slip_id = p.id \
                             left join hr_employee as emp on emp.id = p.employee_id \
                             left join resource_resource as r on r.id = emp.resource_id  \
                            where p.state = 'done' and p.employee_id = %s and (pl.code like %s) and (to_char(date_to,'mm')=%s) and (to_char(date_to,'yyyy')=%s) \
                            group by r.name, p.date_to,emp.id",(emp_id, cod_id, mes, ano,))  
        
        max = self.cr.fetchone()
        
        if max is None:
        	emp_salary.append(0.00)
        else:
        	emp_salary.append(max[0])

        return emp_salary


    def get_employee2(self, form):
        emp_salary = []
        salary_list = []
        last_year = form['end_date'][0:4]
        last_month = form['end_date'][5:7]
        cont = 0



        self.cr.execute("select emp.id, emp.identification_id, emp.name_related \
                             from hr_payslip as p left join hr_employee as emp on emp.id = p.employee_id   \
                             left join hr_contract as r on r.id = p.contract_id  \
                            where p.state = 'done'  and (to_char(date_to,'mm')=%s)   \
                            and (to_char(date_to,'yyyy')=%s)  \
                            group by emp.id, emp.name_related, emp.identification_id order by name_related",( last_month, last_year,))  
    
        id_data = self.cr.fetchall()
        if id_data is None:
            emp_salary.append(0.00)
            emp_salary.append(0.00)
            emp_salary.append(0.00)
            emp_salary.append(0.00)
            emp_salary.append(0.00)
        else:
            for index in id_data:
                emp_salary.append(id_data[cont][0])
                emp_salary.append(id_data[cont][1])
                emp_salary.append(id_data[cont][2])
                emp_salary = self.get_worked_days(form, id_data[cont][0], emp_salary, last_month, last_year )
                emp_salary = self.get_salary(id_data[cont][0], emp_salary, 'BASIC', last_month, last_year )
                emp_salary = self.get_salary(id_data[cont][0], emp_salary, 'HEX%', last_month, last_year )
                emp_salary = self.get_salary(id_data[cont][0], emp_salary, 'GRAT', last_month, last_year )
                emp_salary = self.get_salary(id_data[cont][0], emp_salary, 'BONO', last_month, last_year )
                emp_salary = self.get_salary(id_data[cont][0], emp_salary, 'TOTIM', last_month, last_year )
                emp_salary = self.get_salary(id_data[cont][0], emp_salary, 'ASIGFAM', last_month, last_year )
                emp_salary = self.get_salary(id_data[cont][0], emp_salary, 'TOTNOI', last_month, last_year )
                emp_salary = self.get_salary(id_data[cont][0], emp_salary, 'TOTNOI', last_month, last_year )
                emp_salary = self.get_salary(id_data[cont][0], emp_salary, 'HAB', last_month, last_year )

                cont = cont + 1
                salary_list.append(emp_salary)
                
                emp_salary = []
        
        return salary_list






    def get_employee(self, form):
        emp_salary = []
        salary_list = []
        last_year = form['end_date'][0:4]
        last_month = form['end_date'][5:7]
        cont = 0



        self.cr.execute("select emp.id, emp.identification_id, emp.name_related \
                             from hr_payslip as p left join hr_employee as emp on emp.id = p.employee_id   \
                             left join hr_contract as r on r.id = p.contract_id  \
                            where p.state = 'done'  and (to_char(date_to,'mm')=%s)   \
                            and (to_char(date_to,'yyyy')=%s)  \
                            group by emp.id, emp.name_related, emp.identification_id order by name_related",( last_month, last_year,))  
    
        id_data = self.cr.fetchall()
        if id_data is None:
            emp_salary.append(0.00)
            emp_salary.append(0.00)
            emp_salary.append(0.00)
            emp_salary.append(0.00)
            emp_salary.append(0.00)
        else:
            for index in id_data:
                emp_salary.append(id_data[cont][0])
                emp_salary.append(id_data[cont][1])
                emp_salary.append(id_data[cont][2])
                emp_salary = self.get_worked_days(form, id_data[cont][0], emp_salary, last_month, last_year )
                emp_salary = self.get_salary(id_data[cont][0], emp_salary, 'PREV', last_month, last_year )
                emp_salary = self.get_salary(id_data[cont][0], emp_salary, 'SALUD', last_month, last_year )
                emp_salary = self.get_salary(id_data[cont][0], emp_salary, 'IMPUNI', last_month, last_year )
                emp_salary = self.get_salary(id_data[cont][0], emp_salary, 'SECE', last_month, last_year )
                emp_salary = self.get_salary(id_data[cont][0], emp_salary, 'ADISA', last_month, last_year )
                emp_salary = self.get_salary(id_data[cont][0], emp_salary, 'TODELE', last_month, last_year )
                emp_salary = self.get_salary(id_data[cont][0], emp_salary, 'SMT', last_month, last_year )
                emp_salary = self.get_salary(id_data[cont][0], emp_salary, 'TDE', last_month, last_year )
                emp_salary = self.get_salary(id_data[cont][0], emp_salary, 'LIQ', last_month, last_year )

                cont = cont + 1
                salary_list.append(emp_salary)
                
                emp_salary = []
        
        return salary_list






class wrapped_report_employee_salary_bymonth(osv.AbstractModel):
    _name = 'report.l10n_cl_hr_payroll.report_hrsalarybymonth'
    _inherit = 'report.abstract_report'
    _template = 'l10n_cl_hr_payroll.report_hrsalarybymonth'
    _wrapped_report_class = report_hr_salary_employee_bymonth

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
