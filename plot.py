#coding: utf-8
import os
import matplotlib.pyplot as plt
rooms=['LUNES','MARTES', 'MIERCOLES', 'JUEVES', 'VIERNES', 'SABADO']
colors=['pink', 'lightgreen', 'lightblue', 'wheat', 'lightgrey', 'turquoise']

#input_files=['data1.txt']
#input_files=['schedule1of6']


input_files = [] 

dirname = os.getcwd() + "/results"
for f in os.listdir(dirname):
    input_files.append(f)
    print(f)

print(input_files)




#for input_file, day_label in zip(input_files, day_labels):
for input_file in input_files: 
    
    # TODO: make this better
    courseList = []

    fig=plt.figure(figsize=(10, 7.89))

    relative_path = "results/" + input_file
    for line in open(relative_path, 'r'):
    #for line in open(input_file, 'r'):
        data=line.split()

        event=data[-1]
        data=list(map(float, data[:-1]))

        if event not in courseList:
            courseList.append(event)

        room=data[0]-0.48
        start=data[1]+data[2]/60
        #end=start+data[3]/60
        end=data[3] + data[4]/60
        

	# plot event
        #plt.fill_between([room, room+0.96], [start, start], [end,end], color=colors[int(data[0]-1)], edgecolor='k', linewidth=0.5)
        plt.fill_between([room, room+0.96], [start, start], [end,end], color=colors[courseList.index(event)], edgecolor='k', linewidth=0.5)
        # plot beginning time & end time
        #plt.text(room+0.02, start+0.05 ,'{0}:{1:0>2}'.format(int(data[1]),int(data[2])), va='top', fontsize=7)
        
        plt.text(room+0.02, start+0.05 ,'{0}:{1:0>2} - {2}:{3:0>2}'.format(int(data[1]),int(data[2]), int(data[3]), int(data[4])), va='top', fontsize=7)
        # plot event name
        plt.text(room+0.48, (start+end)*0.5, event, ha='center', va='center', fontsize=11)

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


    #plt.title(day_label,y=1.07)
    #plt.show()
    #input("Press enter to continue")
    #plt.savefig('{0}.png'.format(day_label), dpi=200)
    save_name = input_file + ".png"
    plt.savefig(save_name, dpi=200)
    print("Saved: " + save_name)





