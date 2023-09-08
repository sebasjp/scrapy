
# model coeficients
dict_coef_sugerido = {
    'intercept': 2210608.9115094845,
    'tipo_inmueble': -431981.8500707201, 
    'habitaciones': -151703.01852828087, 
    'banos': 88635.77399214172, 
    'estacionamientos': 9122.063875883927, 
    'antiguedad': -13023.557590620434, 
    'estrato_social': 715944.1043142233
}
dict_coef_li = {
    'intercept': 2139219.9608578617, 
    'tipo_inmueble': -449241.951594261, 
    'habitaciones': -158136.711068016, 
    'banos': 63147.176115728136, 
    'estacionamientos': -32863.7624431249, 
    'antiguedad': -10342.36907914927, 
    'estrato_social': 687842.4827762519
}
dict_coef_ls = {
    'intercept': 2199461.3654100196, 
    'tipo_inmueble': -372588.79974851036, 
    'habitaciones': -114370.53331660278, 
    'banos': 89354.17965816343, 
    'estacionamientos': 31854.8695877798, 
    'antiguedad': -15320.232461070835, 
    'estrato_social': 756562.8490422469
}
# data
import json
f = open('inmuebles-meli/automatizacion/input.json')
data = json.load(f)
f.close()

results_m2 = {
    "precio_sugerido": [], 
    "precio_li": [], 
    "precio_ls": []
}
for var in dict_coef_sugerido.keys():

    if "intercept"==var:
        factor = 1
    else:
        factor = data[var]

    results_m2["precio_sugerido"].append(dict_coef_sugerido[var] * factor)
    results_m2["precio_li"].append(dict_coef_li[var] * factor)
    results_m2["precio_ls"].append(dict_coef_ls[var] * factor)

results = {    
    "precio_li": round(sum(results_m2["precio_li"]) * data["area"]),
    "precio_sugerido": round(sum(results_m2["precio_sugerido"]) * data["area"]),
    "precio_ls": round(sum(results_m2["precio_ls"]) * data["area"])
}
results
