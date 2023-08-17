from sfparamgen import SymFuncParamGenerator

myGenerator = SymFuncParamGenerator(elements=['C', 'Si'], r_cutoff = 7.)
myGenerator.symfunc_type = 'radial'
myGenerator.generate_radial_params(rule='imbalzano2018', mode='shift', nb_param_pairs=8)
myGenerator.write_settings_overview()

myGenerator.write_parameter_strings()

myGenerator.symfunc_type = 'angular_narrow'
myGenerator.zetas = [1.0, 6.0]

myGenerator.generate_radial_params(rule='gastegger2018', mode='center', nb_param_pairs=3, r_lower=0.5)

myGenerator.write_settings_overview()
myGenerator.write_parameter_strings()

myGenerator.symfunc_type='angular_wide'
myGenerator.generate_radial_params(rule='imbalzano2018', mode='center', nb_param_pairs=4)
myGenerator.write_settings_overview()
myGenerator.write_parameter_strings()



myGenerator.symfunc_type='weighted_angular'
myGenerator.generate_radial_params(rule='imbalzano2018', mode='center', nb_param_pairs=4)
myGenerator.write_settings_overview()
myGenerator.write_parameter_strings()


myGenerator.symfunc_type = 'radial'
myGenerator.generate_radial_params(rule='gastegger2018', mode='center', nb_param_pairs=8, r_lower=0.5)
myGenerator.write_settings_overview()

myGenerator.write_parameter_strings()
