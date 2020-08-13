#coding: utf-8
import os
import random
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from shutil import rmtree

rooms=['LUNES','MARTES', 'MIERCOLES', 'JUEVES', 'VIERNES', 'SABADO']
colors=['pink', 'lightgreen', 'lightblue', 'wheat', 'lightgrey', 
	'turquoise', 'antiquewhite', 'aliceblue', 'lightsalmon', 'tomato',
	'firebrick', 'lemonchiffon']

#input_files=['data1.txt']
#input_files=['schedule1of6']


input_files = [] 

dirname = os.getcwd() + "/results"
for f in os.listdir(dirname):
    input_files.append(f)
    #print(f)
random.shuffle(input_files)


#print(input_files)

dname = "images"
if os.path.exists(dname):
    rmtree(dname)
os.makedirs(dname)

#for input_file, day_label in zip(input_files, day_labels):
for input_file in input_files: 
    
    # TODO: make this better
    courseList = []

    fig=plt.figure(figsize=(10, 7.89))

    relative_path = "results/" + input_file
    for line in open(relative_path, 'r'):
        data=line.split()

        eventCID = data[-3]
        event = eventCID 
        eventSection = data[-2] 
        eventType = data[-1]
 
        data=list(map(float, data[:-3]))

        # Only first 5 letters
        if len(event) > 5:
            event = event[:5] 
        event = event + " " + eventSection + " " + eventType 

        if eventCID not in courseList:
            courseList.append(eventCID)

        room=data[0]-0.48
        start=data[1]+data[2]/60
        #end=start+data[3]/60
        end=data[3] + data[4]/60
        

        plt.fill_between([room, room+0.96], [start, start], 
                        [end,end], color=colors[courseList.index(eventCID)-1], 
                        edgecolor='k', linewidth=0.5)
        
        plt.text(room+0.02, start+0.05 ,'{0}:{1:0>2} - {2}:{3:0>2}'.format(int(data[1]),
                        int(data[2]), int(data[3]), int(data[4])), va='top', fontsize=7)
        
	# plot event name
        plt.text(room+0.48, (start+end)*0.5, event, ha='center', va='center', fontsize=9)

    # Set Axis
    ax=fig.add_subplot(111)
    ax.yaxis.grid()
    ax.set_xlim(0.5,len(rooms)+0.5)
    ax.set_ylim(22.1, 6.9) # This is where hours are set
    ax.set_xticks(range(1,len(rooms)+1))
    ax.set_xticklabels(rooms)
    ax.set_ylabel('Time')

    # Set Second Axis
    ax2=ax.twiny().twinx()
    ax2.set_xlim(ax.get_xlim())
    ax2.set_ylim(ax.get_ylim())
    ax2.set_xticks(ax.get_xticks())
    ax2.set_xticklabels(rooms)
    ax2.set_ylabel('Time')
    
    save_name = input_file + ".png"
    plt.savefig(dname + "/" + save_name, dpi=150)
    plt.close(fig)
    print("Saved: " + save_name)





