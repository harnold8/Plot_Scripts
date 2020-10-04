clear
clc
close all

%data for the plume visualization
cd plume1;
plume=dlmread('densitymap.txt');
cd ../plume2;
plume2=dlmread('densitymap.txt');
cd ../plume3;
plume3=dlmread('densitymap.txt');
cd ../plume4;
plume4=dlmread('densitymap.txt');
cd ..;

%trajectory data
traj=dlmread('trajx-1.3');
traj2=dlmread('trajz-1.3');
traj3=dlmread('trajz1.3');

f = figure();
%mapping texture onto sphere
original=imread('europa2.tif');
original = flipdim(original ,2);
[x,y,z]=ellipsoid(0,0,0,1,1,1,300);
surf(x,y,-z);
h=findobj('Type','surface');
set(h,'CData',original,'Facecolor','texturemap','edgecolor','none','HandleVisibility','off');
rotate(h,[0 0 1],-270);
axis equal;
hold on;

%setting background colors
set(gcf,'color','white');
set(gca,'color','black');

%plot extensions
min1=-3;
max1=3;
axis([min1 max1 min1 max1 min1 max1]);

%trajectories
%blue
plot3(traj(:,1),traj(:,2),traj(:,3),'-.','color',[0, 0.4470, 0.7410],'linewidth',1.7);
%red
plot3(traj2(:,1),traj2(:,2),traj2(:,3),'--','color',[0.717,0.11,0.11],'linewidth',1.7);
%green
plot3(traj3(:,1),traj3(:,2),traj3(:,3),'-','color',[0.19,0.717,0.11],'linewidth',1.7);
%violet
plot3([-0.83,-0.83],[-12,12],[-0.89,-0.89],':','color',[0.49,0.129,0.60],'linewidth',1.7);

%cylinders
%creating a standard cylinder
[X,Y,Z] = cylinder(.3,50)
l=length(X);
Z=Z*3;
alpha=pi/4;

%shifting them for different trajectories

%red
h=surf(X-1.3,Y,Z);
set(h,'edgecolor','none','facecolor',[0.717,0.11,0.11])
set(h,'FaceAlpha',0.5)
Z=Z*(-1);
h=surf(X-1.3,Y,Z);
set(h,'edgecolor','none','facecolor',[0.717,0.11,0.11])
set(h,'FaceAlpha',0.5)

%green
h=surf(X+1.3,Y,Z*3);
set(h,'edgecolor','none','facecolor',[0.19,0.717,0.11])
set(h,'FaceAlpha',0.5)
h=surf(X+1.3,Y,Z*-3);
set(h,'edgecolor','none','facecolor',[0.19,0.717,0.11])
set(h,'FaceAlpha',0.5)

%blue
h=surf(Z*3,X,Y-1.3);
set(h,'edgecolor','none','facecolor',[0, 0.4470, 0.7410])
set(h,'FaceAlpha',0.5)
h=surf(Z*-3,X,Y-1.3);
set(h,'edgecolor','none','facecolor',[0, 0.4470, 0.7410])
set(h,'FaceAlpha',0.5)

%violet
h=surf(X-0.83,Z*3,Y-0.89);
set(h,'edgecolor','none','facecolor',[0.49,0.129,0.60])
set(h,'FaceAlpha',0.5)
h=surf(X-0.83,Z*-3,Y-0.89);
set(h,'edgecolor','none','facecolor',[0.49,0.129,0.60])
set(h,'FaceAlpha',0.5)

%the arrows next to the cylinder, to indicate the flight direction
n=length(traj2(:,1))
mArrow3([max1-.8 traj(1,2) traj(1,3)-.5],[max1 traj(1,2) traj(1,3)-.5],'color',[0, 0.4470, 0.7410],'stemWidth',0.013);
mArrow3([traj2(1,1)-.5 traj2(1,2) max1-.8],[traj2(1,1)-.5 traj2(1,2) max1],'color',[0.717,0.11,0.11],'stemWidth',0.013);
mArrow3([traj3(1,1)-.5 traj3(1,2) max1-.8],[traj3(1,1)-.5 traj3(1,2) max1],'color',[0.19,0.717,0.11],'stemWidth',0.013);
mArrow3([-.83 max1-.8 -0.89-.5],[-.83 max1 -0.89-.5],'color',[0.49,0.129,0.60],'stemWidth',0.013);

%viewingangle for the plot
phi=-33.;
theta=22.;

%the plumes emanating from the moon's surface
plot3(plume2(:,1),plume2(:,2),plume2(:,3),'.','color',[0, 0.4470, 0.7410]);
plot3(plume(:,1),plume(:,2),plume(:,3),'.','color',[0.717,0.11,0.11]);
plot3(plume3(:,1),plume3(:,2),plume3(:,3),'.','color',[0.19,0.717,0.11]);
plot3(plume4(:,1),plume4(:,2),plume4(:,3),'.','color',[0.49,0.129,0.60]);


view([phi theta]);
set(gcf,'units','centimeters','PaperPosition',[0 0 15 8]);
fig = gcf;
fig.InvertHardcopy = 'off';
string="trajectories.png"
print(gcf,string,'-dpng','-r500');
