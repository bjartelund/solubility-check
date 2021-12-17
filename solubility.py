#!/usr/bin/python
# vim: set fileencoding = utf-8 :
import csv
#######################
#Data
chemicals = []
formulas = {}
for line in open("formulas.tsf").readlines():
	fields = line.split(",")
	formulas[fields[0]] = fields[1]





#########
def create_ions():
	compounds = open("solubility.tsf").readlines()
	for compound in compounds:
		fields  =  compound.split()
		formula = fields[0]
		i_ions = ions()
		formula_cations,formula_anions = i_ions.get_ions(formula)
		solubility = fields[1]
		chemicals.append(chemical(formula,formula_cations,formula_anions,solubility))
	#for a in chemicals:
	#	print ("%s - %f") % (a.formula,float(a.solubility))
	#	print a.anions
	#	print a.cations

class chemical(list):
	def __init__(self,formula = None,cations=[],anions=[],solubility=0):
		self.formula = formula
		self.cations = cations
		self.anions = anions
		self.solubility = solubility


def rset(seq):
	#Returns only duplicates in a list. a reversed-set.
	nonduplicate = list(set(seq))
	for item in nonduplicate:
		seq.remove(item)
	return seq
class ions:
	def __init__(self):
		cations = ['Al', 'NH4', 'Sb', 'As', 'Ba', 'Bi', 'Cd', 'Ca', 'Cr', 'Co', 'Cu', 'Fe', 'Pb', 'Mg', 'Hg', 'Ni', 'K', 'Ag', 'Na', 'Sr', 'Zn', 'Zr', 'Tl',"Pd"]
		anions = ['AsO4', 'BO3', 'B4O7', 'BrO3', 'BrO', 'CO3', 'CN', 'C2O4', 'C2H3O2', 'C4H4O6', 'ClO4', 'ClO3', 'ClO2', 'ClO', 'CrO4', 'Cr2O7', 'IO4', 'IO3', 'IO', 'HCO3', 'HSO4', 'HSO3', 'HC2O4', 'HPO4', 'H2PO4', 'HS', 'MnO4', 'NH2', 'NO3', 'NO2', 'OH', 'O2', 'PO4', 'PO3', 'SCN', 'S2O3', 'SO4', 'SO3', 'SeO4', 'SiF6', 'SiO3', 'NO3', 'SO4', 'Cl', 'Br', 'I', 'S2', 'C2H3O2', 'CO3']
		self.cations = cations
		self.anions = anions
	
		
	def get_ions(self,formel):
		formula_cations,formula_anions = [],[]
	#cations = [cation.replace("\n","") for cation in (os.popen("echo '%s'|grep -f cations -o" % formel).readlines())]
		for cation in self.cations:
			if cation in formel:
				formula_cations.append(cation)
		for anion in self.anions:
			if anion in formel:
				formula_anions.append(anion)
	
	#anions = [anion.replace("\n","") for anion in (os.popen("echo '%s'|grep -f anions -o" % formel).readlines())]
#		print "Delt i %s og %s" % (str(formula_cations),str(formula_anions))
		return (formula_cations,formula_anions)

def get_formulas(cation,anion):
	#cursor.execute("SELECT formula,solubility FROM formulas WHERE cation = ? AND anion=?",(cation,anion))
	#return cursor.fetchone()
	for formula in chemicals:
		if cation in formula.cations and anion in formula.anions:
			#print "%s - %f" % (formula.formula,float(formula.solubility))
			return (formula.formula,float(formula.solubility))
		
if __name__  == "__main__":
	anions,cations = [],[]
	wells = {}
	create_ions()
	print u"Hva slags stoff har du i løsning?"
	while 1:
		formel = raw_input("Formel:")
		if not formel:
			break
		parts =  ions().get_ions(formel)
		anions+= parts[1]
		cations+= parts[0]
	print "Har du et reservoir-design?"
	reservoirdesign = raw_input("filename:")
	if reservoirdesign:
		designreader = csv.reader(open(reservoirdesign))
		for row in designreader:
			if len(row)  == 7 and row[0].isdigit(): #All valid reservoir-designs from Rigaku has 7 fields, and the first one an integer.
				name = row[-2] #Nest siste felt er navnet
				try:
					formel = formulas[name]
					well = row[0]
					if  wells.has_key(row[0]):
						formula_ions = ions().get_ions(formel)
						try:
							wells[well][0]  =  wells[well][0]+(formula_ions[0])
							wells[well][1]  =  wells[well][1]+(formula_ions[1])
						except TypeError: #Burde fungere alikevel
							pass 
					else:
						wells[well] = ions().get_ions(formel)
						try:
							wells[well][0]  = wells[well][0] + cations
							wells[well][1]  = wells[well][1] + anions
						except:
							pass
				except KeyError:
					print "%s ikke funnet" % name
	for well in wells:
		if well and len(well) > 1:
			for cation in wells[well][0]:
				for anion in wells[well][1]:
					#print (cation,anion)
					result = get_formulas(cation,anion)
					#print result
					if result:
						if result[1] < 10:
							print well
							print u"%s har lav løselighet: %f" % result

	produkter = []
	for anion in anions:
		for cation in cations:
			result  =  get_formulas(cation,anion)
			if result:
				produkter.append(result[0])
				if result[1] < 10:
					print u"%s har lav løselighet: %f" % result
