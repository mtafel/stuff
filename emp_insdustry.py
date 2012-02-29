#/urs/bin/env python
#3/3/2010
#BACKUPTESTCOMMENT

import cairo, math, random
import CairoPlot
import pg

def makepercent_nodata(z):
      #if z <> 0:  
         
         z = str(int(z))+'%' 
         return z
      #else:
       #  z = "No Data"
        # return z


db = pg.connect(dbname = 'database_name', host= 'host', port= 5432, user = 'user',passwd= 'password')

jurisSql = "SELECT * FROM jurisdictions"
jurisSel = db.query(jurisSql) 
jurisResult = jurisSel.getresult()
rows = len(jurisResult)
juris_list = []
x = 0
while x < rows:
 
 jurisRow =  jurisResult[x]
 loc_id = jurisRow[0]
 
 juris_list.append(loc_id)
 
 x=x+1  


juris_list.remove(2)
juris_list.remove(71)
juris_list.remove(47)

selectallSqlReg = "SELECT j.jurisd, v.industry, v.percent FROM jurisdictions j, emp_ind v WHERE j.loc_id = v.loc_id AND j.loc_id = 2 order by industry"


sel = db.query(selectallSqlReg)   
result = sel.getresult()
print result 
#Extractive Activities for Region
row_reg_exa = result[2]
reg_exa = row_reg_exa[2]*100
#Utilities and Construction for Region
row_reg_uc = result[9]
reg_uc = row_reg_uc[2]*100
#Retail and Trade for Region
row_reg_retail = result[8]
reg_retail = row_reg_retail[2]*100
#Public Administration for Region
row_reg_pa = result[7]
reg_pa = row_reg_pa[2]*100
#Professional Services for Region
row_reg_ps = result[6]
reg_ps = row_reg_ps[2]*100
#Personal Services for Region
row_reg_perserv = result[5]
reg_perserv = row_reg_perserv[2]*100
#Manufacturing for Region
row_reg_man = result[3]
reg_man = row_reg_man[2]*100
#Business Services for Region 
row_reg_bus = result[1]
reg_bus = row_reg_bus[2]*100
#Wholesale Trade Transporation and Warehousing for Region
row_reg_wttw = result[0]
reg_wttw = row_reg_wttw[2]*100
#Other for Region
row_reg_other = result[4]
reg_other = row_reg_other[2]*100


for n in juris_list:
   juris = n
   print juris  

   
   


   selectallSql = "SELECT j.jurisd, v.industry, v.percent FROM jurisdictions j, emp_ind v WHERE j.loc_id = v.loc_id AND j.loc_id = %(juris)d ORDER BY v.industry"  % {'juris' : juris}
   
   

   sel_nonReg = db.query(selectallSql)
   result_nonReg = sel_nonReg.getresult()
   
   #Extractive Activities for Jurisdiction
   row_exa = result_nonReg[2]
   exa = row_exa[2]*100
   if exa == -100:
      exa = 0
   else:
      pass
   name = row_exa[0]
   #Utilities and Construction for Jurisdiction
   row_uc = result_nonReg[9]
   uc = row_uc[2]*100
   if uc == -100:
      uc = 0
   else:
      pass
   #Retail and Trade for Jurisdiction
   row_retail = result_nonReg[8]
   retail = row_retail[2]*100
   if retail == -100:
      retail = 0
   else:
      pass
   #Public Administration for Jurisdiction
   row_pa = result_nonReg[7]
   pa = row_pa[2]*100
   if pa == -100:
      pa = 0
   else:
      pass
   #Professional Services for Jurisdiction
   row_ps = result_nonReg[6]
   ps = row_ps[2]*100
   if ps == -100:
      ps = 0
   else:
      pass
   #Personal Services for Jurisdiction
   row_perserv = result_nonReg[5]
   perserv = row_perserv[2]*100
   if perserv == -100:
      perserv = 0
   else: 
      pass
   #Manufacturing for Jurisdiciton
   row_man = result_nonReg[3]
   man = row_man[2]*100
   if man == -100:
      man = 0
   else: 
      pass

   #Business Services for Jurisdiction

   row_bus = result_nonReg[1]
   bus = row_bus[2]*100
   if bus == -100:
      bus = 0
   else:
      pass
   #Wholesale Trade Transporation and Warehousing for Jurisdiction
   
   row_wttw = result_nonReg[0]
   wttw = row_wttw[2]*100
   if wttw == -100:
      wttw = 0
   else: 
      pass 
  #Other for Jurisdiction
   row_other = result_nonReg[4]
   other = row_other[2]*100
   if other == -100:
      other = 0
   else:
      pass 
#"dark_purple" : (0.0,0.29,0.14,0.67), "light_purple" : (0.0,0.33,0.13,0.04),
   
   if name == "Unincorporated Adams County":
       name = "Uninc. Adams County"
   else:
       pass
   if name == "Unincorporated Arapahoe County":
       name = "Uninc. Arapahoe County"
   else:
       pass
   if name == "Unincorporated Boulder County":
       name = "Uninc. Boulder County"
   else:
       pass
   if name == "Unincorporated Clear Creek County":
       name = "Uninc. Clear Creek County"
   else: 
       pass
   if name == "Unincorporated Douglas County":
       name = "Uninc. Douglas County"
   else:
       pass
   if name == "Unincorporated Gilpin County":
       name = "Uninc. Gilpin County"
   else:
       pass
   if name == "Unincorporated Jefferson County":
       name = "Uninc. Jefferson County" 
   else:
       pass
   
   series_labels = [name, "Region"]
   colors = ["light_blue", "Navy" ]
   data = [[other, reg_other], [wttw, reg_wttw], [bus, reg_bus], [man, reg_man], [perserv, reg_perserv], [ps, reg_ps], [pa, reg_pa], [retail, reg_retail], [uc, reg_uc], [exa, reg_exa]]
  
   #x_labels = [ "line1", "line2", "line3", "line4", "line5", "line6" ]
   #background = (1.0,0.0,1.0,1.0)
   y_labels = [ "Other", "Wholesale Trade", "Business Services", "Manufacturing", "Personal Services", "Professional Services", "Public Administration", "Retail Trade", "Utilities & Construction", "Extractive Activities" ]
 
   CairoPlot.horizontal_bar_plot (  '/home/michael/Documents/comm_prof/emp_by_ind/'+name+'.pdf', data, 380, 230, background = "white",border = 20,  display_values = True, grid = False, y_labels = y_labels, series_labels = series_labels, colors = colors, value_formatter = lambda x: makepercent_nodata(x))
 
#series_labels = series_labels
#value_formatter = lambda x: addcomma(x) 
   #'smb://cognet%2Fmtafel@kennedy/crs/Community%20Profiles_2010_2011/charts/hh_type'+name+'hh_type.png'
   # '/home/michael/Documents/comm_prof/hh_type/'
 
    
      #x_labels = x_labels
 # plt.savefig("/home/michael/Pictures/"+name+"_household.png")



