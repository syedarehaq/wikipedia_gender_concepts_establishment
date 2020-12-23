#!/bin/bash
## From c3178 to c3224 we have in total 47 netsi standard nodes
## in python " ".join(["c3%d"%x for x in range(178,224+1)])
for nodename in c3178 c3179 c3180 c3181 c3182 c3183 c3184 c3185 c3186 c3187 c3188 c3189 c3190 c3191 c3192 c3193 c3194 c3195 c3196 c3197 c3198 c3199 c3200 c3201 c3202 c3203 c3204 c3205 c3206 c3207 c3208 c3209 c3210 c3211 c3212 c3213 c3214 c3215 c3216 c3217 c3218 c3219 c3220 c3221 c3222 c3223 c3224
#for nodename in c3178 c3179
do
	screen -dmS $nodename"_pythonsearch" bash -c "bash python_search_single_ssh.sh "$nodename"; exec sh;" &
done