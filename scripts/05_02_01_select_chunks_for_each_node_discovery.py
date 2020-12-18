# -*- coding: utf-8 -*-

"""
Summary:
    In this script I am creating 47 chunks of files assigned
    to each one of the single nodes I will be using in discvery
    to run the search process in wikipedia
Input:
    None
Output
    It will create a text file for each of the 47 nodes,
    newline separated, containing the input file they 
    will work on
"""
from collections import defaultdict

# %%
output_code = "05_02_01"

chunks = ["phrases2_min2_20201217_conceptsize_1_chunknum_0.csv",
"phrases2_min2_20201217_conceptsize_1_chunknum_1.csv",
"phrases2_min2_20201217_conceptsize_1_chunknum_2.csv",
"phrases2_min2_20201217_conceptsize_1_chunknum_3.csv",
"phrases2_min2_20201217_conceptsize_1_chunknum_4.csv",
"phrases2_min2_20201217_conceptsize_1_chunknum_5.csv",
"phrases2_min2_20201217_conceptsize_1_chunknum_6.csv",
"phrases2_min2_20201217_conceptsize_1_chunknum_7.csv",
"phrases2_min2_20201217_conceptsize_1_chunknum_8.csv",
"phrases2_min2_20201217_conceptsize_1_chunknum_9.csv",
"phrases2_min2_20201217_conceptsize_1_chunknum_10.csv",
"phrases2_min2_20201217_conceptsize_1_chunknum_11.csv",
"phrases2_min2_20201217_conceptsize_1_chunknum_12.csv",
"phrases2_min2_20201217_conceptsize_1_chunknum_13.csv",
"phrases2_min2_20201217_conceptsize_1_chunknum_14.csv",
"phrases2_min2_20201217_conceptsize_1_chunknum_15.csv",
"phrases2_min2_20201217_conceptsize_1_chunknum_16.csv",
"phrases2_min2_20201217_conceptsize_1_chunknum_17.csv",
"phrases2_min2_20201217_conceptsize_1_chunknum_18.csv",
"phrases2_min2_20201217_conceptsize_1_chunknum_19.csv",
"phrases2_min2_20201217_conceptsize_1_chunknum_20.csv",
"phrases2_min2_20201217_conceptsize_1_chunknum_21.csv",
"phrases2_min2_20201217_conceptsize_1_chunknum_22.csv",
"phrases2_min2_20201217_conceptsize_1_chunknum_23.csv",
"phrases2_min2_20201217_conceptsize_1_chunknum_24.csv",
"phrases2_min2_20201217_conceptsize_1_chunknum_25.csv",
"phrases2_min2_20201217_conceptsize_1_chunknum_26.csv",
"phrases2_min2_20201217_conceptsize_1_chunknum_27.csv",
"phrases2_min2_20201217_conceptsize_1_chunknum_28.csv",
"phrases2_min2_20201217_conceptsize_1_chunknum_29.csv",
"phrases2_min2_20201217_conceptsize_1_chunknum_30.csv",
"phrases2_min2_20201217_conceptsize_1_chunknum_31.csv",
"phrases2_min2_20201217_conceptsize_1_chunknum_32.csv",
"phrases2_min2_20201217_conceptsize_1_chunknum_33.csv",
"phrases2_min2_20201217_conceptsize_1_chunknum_34.csv",
"phrases2_min2_20201217_conceptsize_1_chunknum_35.csv",
"phrases2_min2_20201217_conceptsize_1_chunknum_36.csv",
"phrases2_min2_20201217_conceptsize_1_chunknum_37.csv",
"phrases2_min2_20201217_conceptsize_1_chunknum_38.csv",
"phrases2_min2_20201217_conceptsize_1_chunknum_39.csv",
"phrases2_min2_20201217_conceptsize_1_chunknum_40.csv",
"phrases2_min2_20201217_conceptsize_1_chunknum_41.csv",
"phrases2_min2_20201217_conceptsize_1_chunknum_42.csv",
"phrases2_min2_20201217_conceptsize_1_chunknum_43.csv",
"phrases2_min2_20201217_conceptsize_1_chunknum_44.csv",
"phrases2_min2_20201217_conceptsize_1_chunknum_45.csv",
"phrases2_min2_20201217_conceptsize_1_chunknum_46.csv",
"phrases2_min2_20201217_conceptsize_1_chunknum_47.csv",
"phrases2_min2_20201217_conceptsize_1_chunknum_48.csv",
"phrases2_min2_20201217_conceptsize_1_chunknum_49.csv",
"phrases2_min2_20201217_conceptsize_1_chunknum_50.csv",
"phrases2_min2_20201217_conceptsize_1_chunknum_51.csv",
"phrases2_min2_20201217_conceptsize_1_chunknum_52.csv",
"phrases2_min2_20201217_conceptsize_1_chunknum_53.csv",
"phrases2_min2_20201217_conceptsize_1_chunknum_54.csv",
"phrases2_min2_20201217_conceptsize_1_chunknum_55.csv",
"phrases2_min2_20201217_conceptsize_1_chunknum_56.csv",
"phrases2_min2_20201217_conceptsize_1_chunknum_57.csv",
"phrases2_min2_20201217_conceptsize_1_chunknum_58.csv",
"phrases2_min2_20201217_conceptsize_2_chunknum_0.csv",
"phrases2_min2_20201217_conceptsize_2_chunknum_1.csv",
"phrases2_min2_20201217_conceptsize_2_chunknum_2.csv",
"phrases2_min2_20201217_conceptsize_2_chunknum_3.csv",
"phrases2_min2_20201217_conceptsize_2_chunknum_4.csv",
"phrases2_min2_20201217_conceptsize_2_chunknum_5.csv",
"phrases2_min2_20201217_conceptsize_2_chunknum_6.csv",
"phrases2_min2_20201217_conceptsize_2_chunknum_7.csv",
"phrases2_min2_20201217_conceptsize_2_chunknum_8.csv",
"phrases2_min2_20201217_conceptsize_2_chunknum_9.csv",
"phrases2_min2_20201217_conceptsize_2_chunknum_10.csv",
"phrases2_min2_20201217_conceptsize_2_chunknum_11.csv",
"phrases2_min2_20201217_conceptsize_2_chunknum_12.csv",
"phrases2_min2_20201217_conceptsize_2_chunknum_13.csv",
"phrases2_min2_20201217_conceptsize_2_chunknum_14.csv",
"phrases2_min2_20201217_conceptsize_2_chunknum_15.csv",
"phrases2_min2_20201217_conceptsize_2_chunknum_16.csv",
"phrases2_min2_20201217_conceptsize_2_chunknum_17.csv",
"phrases2_min2_20201217_conceptsize_2_chunknum_18.csv",
"phrases2_min2_20201217_conceptsize_2_chunknum_19.csv",
"phrases2_min2_20201217_conceptsize_2_chunknum_20.csv",
"phrases2_min2_20201217_conceptsize_2_chunknum_21.csv",
"phrases2_min2_20201217_conceptsize_2_chunknum_22.csv",
"phrases2_min2_20201217_conceptsize_2_chunknum_23.csv",
"phrases2_min2_20201217_conceptsize_2_chunknum_24.csv",
"phrases2_min2_20201217_conceptsize_2_chunknum_25.csv",
"phrases2_min2_20201217_conceptsize_2_chunknum_26.csv",
"phrases2_min2_20201217_conceptsize_2_chunknum_27.csv",
"phrases2_min2_20201217_conceptsize_2_chunknum_28.csv",
"phrases2_min2_20201217_conceptsize_2_chunknum_29.csv",
"phrases2_min2_20201217_conceptsize_2_chunknum_30.csv",
"phrases2_min2_20201217_conceptsize_2_chunknum_31.csv",
"phrases2_min2_20201217_conceptsize_2_chunknum_32.csv",
"phrases2_min2_20201217_conceptsize_2_chunknum_33.csv",
"phrases2_min2_20201217_conceptsize_2_chunknum_34.csv",
"phrases2_min2_20201217_conceptsize_2_chunknum_35.csv",
"phrases2_min2_20201217_conceptsize_2_chunknum_36.csv",
"phrases2_min2_20201217_conceptsize_2_chunknum_37.csv",
"phrases2_min2_20201217_conceptsize_2_chunknum_38.csv",
"phrases2_min2_20201217_conceptsize_2_chunknum_39.csv",
"phrases2_min2_20201217_conceptsize_2_chunknum_40.csv",
"phrases2_min2_20201217_conceptsize_2_chunknum_41.csv",
"phrases2_min2_20201217_conceptsize_2_chunknum_42.csv",
"phrases2_min2_20201217_conceptsize_2_chunknum_43.csv",
"phrases2_min2_20201217_conceptsize_2_chunknum_44.csv",
"phrases2_min2_20201217_conceptsize_2_chunknum_45.csv",
"phrases2_min2_20201217_conceptsize_2_chunknum_46.csv",
"phrases2_min2_20201217_conceptsize_2_chunknum_47.csv",
"phrases2_min2_20201217_conceptsize_2_chunknum_48.csv",
"phrases2_min2_20201217_conceptsize_2_chunknum_49.csv",
"phrases2_min2_20201217_conceptsize_2_chunknum_50.csv",
"phrases2_min2_20201217_conceptsize_2_chunknum_51.csv",
"phrases2_min2_20201217_conceptsize_2_chunknum_52.csv",
"phrases2_min2_20201217_conceptsize_2_chunknum_53.csv",
"phrases2_min2_20201217_conceptsize_2_chunknum_54.csv",
"phrases2_min2_20201217_conceptsize_2_chunknum_55.csv",
"phrases2_min2_20201217_conceptsize_2_chunknum_56.csv",
"phrases2_min2_20201217_conceptsize_2_chunknum_57.csv",
"phrases2_min2_20201217_conceptsize_2_chunknum_58.csv",
"phrases2_min2_20201217_conceptsize_2_chunknum_59.csv",
"phrases2_min2_20201217_conceptsize_2_chunknum_60.csv",
"phrases2_min2_20201217_conceptsize_2_chunknum_61.csv",
"phrases2_min2_20201217_conceptsize_2_chunknum_62.csv",
"phrases2_min2_20201217_conceptsize_2_chunknum_63.csv",
"phrases2_min2_20201217_conceptsize_2_chunknum_64.csv",
"phrases2_min2_20201217_conceptsize_2_chunknum_65.csv",
"phrases2_min2_20201217_conceptsize_2_chunknum_66.csv",
"phrases2_min2_20201217_conceptsize_2_chunknum_67.csv",
"phrases2_min2_20201217_conceptsize_2_chunknum_68.csv",
"phrases2_min2_20201217_conceptsize_2_chunknum_69.csv",
"phrases2_min2_20201217_conceptsize_2_chunknum_70.csv",
"phrases2_min2_20201217_conceptsize_2_chunknum_71.csv",
"phrases2_min2_20201217_conceptsize_2_chunknum_72.csv",
"phrases2_min2_20201217_conceptsize_2_chunknum_73.csv",
"phrases2_min2_20201217_conceptsize_2_chunknum_74.csv",
"phrases2_min2_20201217_conceptsize_2_chunknum_75.csv",
"phrases2_min2_20201217_conceptsize_2_chunknum_76.csv",
"phrases2_min2_20201217_conceptsize_2_chunknum_77.csv",
"phrases2_min2_20201217_conceptsize_2_chunknum_78.csv",
"phrases2_min2_20201217_conceptsize_2_chunknum_79.csv",
"phrases2_min2_20201217_conceptsize_2_chunknum_80.csv",
"phrases2_min2_20201217_conceptsize_2_chunknum_81.csv",
"phrases2_min2_20201217_conceptsize_2_chunknum_82.csv",
"phrases2_min2_20201217_conceptsize_2_chunknum_83.csv",
"phrases2_min2_20201217_conceptsize_2_chunknum_84.csv",
"phrases2_min2_20201217_conceptsize_2_chunknum_85.csv",
"phrases2_min2_20201217_conceptsize_2_chunknum_86.csv",
"phrases2_min2_20201217_conceptsize_2_chunknum_87.csv",
"phrases2_min2_20201217_conceptsize_2_chunknum_88.csv",
"phrases2_min2_20201217_conceptsize_2_chunknum_89.csv",
"phrases2_min2_20201217_conceptsize_2_chunknum_90.csv",
"phrases2_min2_20201217_conceptsize_2_chunknum_91.csv",
"phrases2_min2_20201217_conceptsize_2_chunknum_92.csv",
"phrases2_min2_20201217_conceptsize_2_chunknum_93.csv",
"phrases2_min2_20201217_conceptsize_2_chunknum_94.csv",
"phrases2_min2_20201217_conceptsize_2_chunknum_95.csv",
"phrases2_min2_20201217_conceptsize_2_chunknum_96.csv",
"phrases2_min2_20201217_conceptsize_2_chunknum_97.csv",
"phrases2_min2_20201217_conceptsize_2_chunknum_98.csv",
"phrases2_min2_20201217_conceptsize_2_chunknum_99.csv",
"phrases2_min2_20201217_conceptsize_2_chunknum_100.csv",
"phrases2_min2_20201217_conceptsize_2_chunknum_101.csv",
"phrases2_min2_20201217_conceptsize_2_chunknum_102.csv",
"phrases2_min2_20201217_conceptsize_2_chunknum_103.csv",
"phrases2_min2_20201217_conceptsize_3_chunknum_0.csv",
"phrases2_min2_20201217_conceptsize_3_chunknum_1.csv",
"phrases2_min2_20201217_conceptsize_3_chunknum_2.csv",
"phrases2_min2_20201217_conceptsize_3_chunknum_3.csv",
"phrases2_min2_20201217_conceptsize_3_chunknum_4.csv",
"phrases2_min2_20201217_conceptsize_3_chunknum_5.csv",
"phrases2_min2_20201217_conceptsize_3_chunknum_6.csv",
"phrases2_min2_20201217_conceptsize_3_chunknum_7.csv",
"phrases2_min2_20201217_conceptsize_3_chunknum_8.csv",
"phrases2_min2_20201217_conceptsize_3_chunknum_9.csv",
"phrases2_min2_20201217_conceptsize_3_chunknum_10.csv",
"phrases2_min2_20201217_conceptsize_3_chunknum_11.csv",
"phrases2_min2_20201217_conceptsize_3_chunknum_12.csv",
"phrases2_min2_20201217_conceptsize_3_chunknum_13.csv",
"phrases2_min2_20201217_conceptsize_3_chunknum_14.csv",
"phrases2_min2_20201217_conceptsize_3_chunknum_15.csv",
"phrases2_min2_20201217_conceptsize_3_chunknum_16.csv",
"phrases2_min2_20201217_conceptsize_3_chunknum_17.csv",
"phrases2_min2_20201217_conceptsize_3_chunknum_18.csv",
"phrases2_min2_20201217_conceptsize_3_chunknum_19.csv",
"phrases2_min2_20201217_conceptsize_3_chunknum_20.csv",
"phrases2_min2_20201217_conceptsize_3_chunknum_21.csv",
"phrases2_min2_20201217_conceptsize_4_chunknum_0.csv",
"phrases2_min2_20201217_conceptsize_4_chunknum_1.csv",
"phrases2_min2_20201217_conceptsize_4_chunknum_2.csv",
"phrases2_min2_20201217_conceptsize_4_chunknum_3.csv",
"phrases2_min2_20201217_conceptsize_5_chunknum_0.csv",
"phrases3_min3_20201217_conceptsize_1_chunknum_0.csv",
"phrases3_min3_20201217_conceptsize_1_chunknum_1.csv",
"phrases3_min3_20201217_conceptsize_1_chunknum_2.csv",
"phrases3_min3_20201217_conceptsize_1_chunknum_3.csv",
"phrases3_min3_20201217_conceptsize_1_chunknum_4.csv",
"phrases3_min3_20201217_conceptsize_1_chunknum_5.csv",
"phrases3_min3_20201217_conceptsize_1_chunknum_6.csv",
"phrases3_min3_20201217_conceptsize_1_chunknum_7.csv",
"phrases3_min3_20201217_conceptsize_1_chunknum_8.csv",
"phrases3_min3_20201217_conceptsize_1_chunknum_9.csv",
"phrases3_min3_20201217_conceptsize_1_chunknum_10.csv",
"phrases3_min3_20201217_conceptsize_1_chunknum_11.csv",
"phrases3_min3_20201217_conceptsize_1_chunknum_12.csv",
"phrases3_min3_20201217_conceptsize_1_chunknum_13.csv",
"phrases3_min3_20201217_conceptsize_1_chunknum_14.csv",
"phrases3_min3_20201217_conceptsize_1_chunknum_15.csv",
"phrases3_min3_20201217_conceptsize_1_chunknum_16.csv",
"phrases3_min3_20201217_conceptsize_1_chunknum_17.csv",
"phrases3_min3_20201217_conceptsize_1_chunknum_18.csv",
"phrases3_min3_20201217_conceptsize_1_chunknum_19.csv",
"phrases3_min3_20201217_conceptsize_1_chunknum_20.csv",
"phrases3_min3_20201217_conceptsize_1_chunknum_21.csv",
"phrases3_min3_20201217_conceptsize_1_chunknum_22.csv",
"phrases3_min3_20201217_conceptsize_1_chunknum_23.csv",
"phrases3_min3_20201217_conceptsize_1_chunknum_24.csv",
"phrases3_min3_20201217_conceptsize_1_chunknum_25.csv",
"phrases3_min3_20201217_conceptsize_1_chunknum_26.csv",
"phrases3_min3_20201217_conceptsize_1_chunknum_27.csv",
"phrases3_min3_20201217_conceptsize_1_chunknum_28.csv",
"phrases3_min3_20201217_conceptsize_1_chunknum_29.csv",
"phrases3_min3_20201217_conceptsize_1_chunknum_30.csv",
"phrases3_min3_20201217_conceptsize_1_chunknum_31.csv",
"phrases3_min3_20201217_conceptsize_1_chunknum_32.csv",
"phrases3_min3_20201217_conceptsize_1_chunknum_33.csv",
"phrases3_min3_20201217_conceptsize_1_chunknum_34.csv",
"phrases3_min3_20201217_conceptsize_1_chunknum_35.csv",
"phrases3_min3_20201217_conceptsize_1_chunknum_36.csv",
"phrases3_min3_20201217_conceptsize_1_chunknum_37.csv",
"phrases3_min3_20201217_conceptsize_1_chunknum_38.csv",
"phrases3_min3_20201217_conceptsize_1_chunknum_39.csv",
"phrases3_min3_20201217_conceptsize_1_chunknum_40.csv",
"phrases3_min3_20201217_conceptsize_1_chunknum_41.csv",
"phrases3_min3_20201217_conceptsize_1_chunknum_42.csv",
"phrases3_min3_20201217_conceptsize_1_chunknum_43.csv",
"phrases3_min3_20201217_conceptsize_1_chunknum_44.csv",
"phrases3_min3_20201217_conceptsize_1_chunknum_45.csv",
"phrases3_min3_20201217_conceptsize_1_chunknum_46.csv",
"phrases3_min3_20201217_conceptsize_1_chunknum_47.csv",
"phrases3_min3_20201217_conceptsize_1_chunknum_48.csv",
"phrases3_min3_20201217_conceptsize_1_chunknum_49.csv",
"phrases3_min3_20201217_conceptsize_1_chunknum_50.csv",
"phrases3_min3_20201217_conceptsize_1_chunknum_51.csv",
"phrases3_min3_20201217_conceptsize_1_chunknum_52.csv",
"phrases3_min3_20201217_conceptsize_1_chunknum_53.csv",
"phrases3_min3_20201217_conceptsize_1_chunknum_54.csv",
"phrases3_min3_20201217_conceptsize_1_chunknum_55.csv",
"phrases3_min3_20201217_conceptsize_1_chunknum_56.csv",
"phrases3_min3_20201217_conceptsize_1_chunknum_57.csv",
"phrases3_min3_20201217_conceptsize_1_chunknum_58.csv",
"phrases3_min3_20201217_conceptsize_1_chunknum_59.csv",
"phrases3_min3_20201217_conceptsize_1_chunknum_60.csv",
"phrases3_min3_20201217_conceptsize_1_chunknum_61.csv",
"phrases3_min3_20201217_conceptsize_1_chunknum_62.csv",
"phrases3_min3_20201217_conceptsize_1_chunknum_63.csv",
"phrases3_min3_20201217_conceptsize_1_chunknum_64.csv",
"phrases3_min3_20201217_conceptsize_1_chunknum_65.csv",
"phrases3_min3_20201217_conceptsize_1_chunknum_66.csv",
"phrases3_min3_20201217_conceptsize_1_chunknum_67.csv",
"phrases3_min3_20201217_conceptsize_1_chunknum_68.csv",
"phrases3_min3_20201217_conceptsize_1_chunknum_69.csv",
"phrases3_min3_20201217_conceptsize_1_chunknum_70.csv",
"phrases3_min3_20201217_conceptsize_1_chunknum_71.csv",
"phrases3_min3_20201217_conceptsize_2_chunknum_0.csv",
"phrases3_min3_20201217_conceptsize_2_chunknum_1.csv",
"phrases3_min3_20201217_conceptsize_2_chunknum_2.csv",
"phrases3_min3_20201217_conceptsize_2_chunknum_3.csv",
"phrases3_min3_20201217_conceptsize_2_chunknum_4.csv",
"phrases3_min3_20201217_conceptsize_2_chunknum_5.csv",
"phrases3_min3_20201217_conceptsize_2_chunknum_6.csv",
"phrases3_min3_20201217_conceptsize_2_chunknum_7.csv",
"phrases3_min3_20201217_conceptsize_2_chunknum_8.csv",
"phrases3_min3_20201217_conceptsize_2_chunknum_9.csv",
"phrases3_min3_20201217_conceptsize_2_chunknum_10.csv",
"phrases3_min3_20201217_conceptsize_2_chunknum_11.csv",
"phrases3_min3_20201217_conceptsize_2_chunknum_12.csv",
"phrases3_min3_20201217_conceptsize_2_chunknum_13.csv",
"phrases3_min3_20201217_conceptsize_2_chunknum_14.csv",
"phrases3_min3_20201217_conceptsize_2_chunknum_15.csv",
"phrases3_min3_20201217_conceptsize_2_chunknum_16.csv",
"phrases3_min3_20201217_conceptsize_2_chunknum_17.csv",
"phrases3_min3_20201217_conceptsize_2_chunknum_18.csv",
"phrases3_min3_20201217_conceptsize_2_chunknum_19.csv",
"phrases3_min3_20201217_conceptsize_2_chunknum_20.csv",
"phrases3_min3_20201217_conceptsize_2_chunknum_21.csv",
"phrases3_min3_20201217_conceptsize_2_chunknum_22.csv",
"phrases3_min3_20201217_conceptsize_2_chunknum_23.csv",
"phrases3_min3_20201217_conceptsize_2_chunknum_24.csv",
"phrases3_min3_20201217_conceptsize_2_chunknum_25.csv",
"phrases3_min3_20201217_conceptsize_2_chunknum_26.csv",
"phrases3_min3_20201217_conceptsize_2_chunknum_27.csv",
"phrases3_min3_20201217_conceptsize_2_chunknum_28.csv",
"phrases3_min3_20201217_conceptsize_2_chunknum_29.csv",
"phrases3_min3_20201217_conceptsize_2_chunknum_30.csv",
"phrases3_min3_20201217_conceptsize_2_chunknum_31.csv",
"phrases3_min3_20201217_conceptsize_2_chunknum_32.csv",
"phrases3_min3_20201217_conceptsize_2_chunknum_33.csv",
"phrases3_min3_20201217_conceptsize_2_chunknum_34.csv",
"phrases3_min3_20201217_conceptsize_2_chunknum_35.csv",
"phrases3_min3_20201217_conceptsize_2_chunknum_36.csv",
"phrases3_min3_20201217_conceptsize_2_chunknum_37.csv",
"phrases3_min3_20201217_conceptsize_2_chunknum_38.csv",
"phrases3_min3_20201217_conceptsize_2_chunknum_39.csv",
"phrases3_min3_20201217_conceptsize_2_chunknum_40.csv",
"phrases3_min3_20201217_conceptsize_2_chunknum_41.csv",
"phrases3_min3_20201217_conceptsize_2_chunknum_42.csv",
"phrases3_min3_20201217_conceptsize_2_chunknum_43.csv",
"phrases3_min3_20201217_conceptsize_2_chunknum_44.csv",
"phrases3_min3_20201217_conceptsize_2_chunknum_45.csv",
"phrases3_min3_20201217_conceptsize_2_chunknum_46.csv",
"phrases3_min3_20201217_conceptsize_3_chunknum_0.csv",
"phrases3_min3_20201217_conceptsize_3_chunknum_1.csv",
"phrases3_min3_20201217_conceptsize_3_chunknum_2.csv",
"phrases3_min3_20201217_conceptsize_3_chunknum_3.csv",
"phrases3_min3_20201217_conceptsize_3_chunknum_4.csv",
"phrases3_min3_20201217_conceptsize_3_chunknum_5.csv",
"phrases3_min3_20201217_conceptsize_3_chunknum_6.csv",
"phrases3_min3_20201217_conceptsize_3_chunknum_7.csv",
"phrases3_min3_20201217_conceptsize_4_chunknum_0.csv",
"phrases3_min3_20201217_conceptsize_4_chunknum_1.csv",
"phrases3_min3_20201217_conceptsize_5_chunknum_0.csv",]

nodenum_to_filelist = defaultdict(list)
counter = 0
total_discovery_nodes = 47
while chunks:
    nodenum_to_filelist[counter%total_discovery_nodes].append(chunks.pop())
    counter += 1

for current_node, fnames in nodenum_to_filelist.items():
    with open(f"../input/derived/discovery_input_for_each_node/{output_code}_{current_node}.txt","w") as f:
        for fname in fnames:
            f.write(fname+"\n")