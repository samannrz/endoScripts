dict ={ 'evals':[
		{'frame':'P-0137_Video001_trim.mp4',
		 'index': [190]
		},
		{'frame':'P-0146_Video001_trim_1.mp4',
		 'index': [1268]
		},
		{'frame':'P-0146_Video001_trim_2.mp4',
		 'index': [78]
		},
		{'frame':'P-0148_Video007_trim_1.mp4',
		 'index': [305]
		},
		{'frame':'P-0148_Video007_trim_2.mp4',
		 'index': [528]
		},
		{'frame':'P-0170_Video001_trim.mp4',
		 'index': [182]
		},
		{'frame':'P-0170_Video002_trim.mp4',
		 'index': [290]
		},
		{'frame':'P-0170_Video003_trim_1.mp4',
		 'index': [66]
		},
		{'frame':'P-0170_Video003_trim_2.mp4',
		 'index': [171]
		},
		{'frame':'P-0212_Video002_trim.mp4',
		 'index': [887]
		},
		{'frame':'P-0212_Video003_trim_1.mp4',
		 'index': [78]
		},
		{'frame':'P-0212_Video003_trim_2.mp4',
		 'index': [148]
		},
		{'frame':'P-0212_Video004_trim.mp4',
		 'index': [110]
		},
		{'frame':'P-0266_Video001_trim.mp4',
		 'index': [1360]
		},
		{'frame':'P-0266_Video003_trim.mp4',
		 'index': [37]
		}
	]
}
import json
json_object = json.dumps(dict, indent=4)

# Writing to sample.json
with open("Evaluation3.json", "w") as outfile:
	outfile.write(json_object)
