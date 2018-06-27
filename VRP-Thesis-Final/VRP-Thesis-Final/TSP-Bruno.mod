/*********************************************
 * OPL 12.6.2.0 Model
 * Author: MhmdMnsr
 * Creation Date: Nov 30, 2015 at 10:32:11 AM
 *********************************************/
// problem size
int n=...;
//range cities = 1..n;

// generate random data

tuple City{
	int id;
}

//tuple location
//{
//	float x;
//	float y;
//}

tuple edge
{
	int i;
	int j;
	float d;
}

tuple IJ
{
	int i;
	int j;
}

int depot = ...;  


setof(City) indices =...;
setof(int) cities = {idx.id | idx in indices};

setof(edge) edges1 =...;
setof(IJ) edges = {<idx.i,idx.j> | idx in edges1: idx.i!=idx.j};


//setof(edge) edges = {<i,j> | i,j in cities: i!=j};

float c[edges] = [<idx.i,idx.j> : idx.d | idx in edges1];


//float c[edges];
//location cityLocation[cities];

//execute
//{
//	function getDistance(city1,city2)
//	{
//		return Opl.sqrt(Opl.pow(city1.x - city2.x, 2) + Opl.pow(city1.y - city2.y, 2))	
//	}
//
//	for (var i in cities)
//	{
//		cityLocation[i].x = Opl.rand(100);	
//		cityLocation[i].y = Opl.rand(100);	
//	}
//	
//	for (var e in edges)
//	{
//		c[e] = getDistance(cityLocation[e.i],cityLocation[e.j])	
//	}
//}

// decision variable
dvar boolean x[edges];
dvar float u[cities];


//expressions
dexpr float totalDistance = sum(e in edges) c[e]*x[e];
//dexpr float totalDistance = sum(idx in ij) distance[idx]*x[idx];

minimize totalDistance;
subject to
{
	forall (i in indices)
	  flow_in:
	  sum (idx in edges : idx.i == i.id) x[idx] ==1;
	  
  	forall (j in indices)
  	  flow_out:
  	  sum(idx in edges: idx.j == j.id) x[idx] == 1;
  	  
  	  
  	  //The MTZ formulation
  	  u[depot] == 1;
  	  
  	  forall(i in cities: i!= depot){
  	  u[i] >= 2;
  	  u[i] <= n;
  	    	  
  	  }
  	    
  	  
// 	forall (i,j in cities : i!=depot && j!= depot && i!=j)
//  	  subtour:
//  	  u[i]-u[j]+(n-1)*x[<i,j>]<=n-2;
  	  
 	forall (i,j in cities : i!=depot && j!= depot && i!=j)
  	  subtour:
  	  u[i]-u[j]+(n-1)*x[<i,j>]+(n-3)*x[<j,i>]<=n-2; //lifted version of MTZ (DL)
  	  
  	  
}


float solX[0..n-1][0..2];					//matrix for writing the solution of the variables x
float solU [0..n-1][0..1];

execute{

//for the graph
	var row = 0;
  	for (var idx in edges){
  		if(x[idx] != 0){  	
  	
      		solX[row][0] = idx.i;
      		solX[row][1] = idx.j;
      		solX[row][2] = x[idx];
			row ++;
		}		
	}
	
	//for the u''
	
	var row = 0;
	  	for (var i in cities){
  		if(u[i] != 0){  	
  	
      		solU[row][0] = i;
      		solU[row][1] = u[i];
			row ++;
		}		
	}


}




//
//// ---- this part of the code contains the necessary computations for writing the solution into the excel file 
////(note that further on one should use only the database. the methods for the database are already developed down)
//string solX[0..2000][0..3];					//esta  tabela tera 4 colunas (node_i,  node_j, vehicle; value)
//string solTime_k[0..1000][0..2];			//esta  tabela tera 3 colunas (node_i,  chipper; value)
//string solTime_v[0..1000][0..2];			//esta  tabela tera 3 colunas (node_i,  truck; value)
//string solW[0..1000][0..1];					//esta  tabela tera 2 colunas (node_i,   value)
//
//string  outputSolution[0..5000][0..4];		//this tabe has 5 columns (idlocation, idVehilce, arrivaltime, departure time, waiting)
//
//execute {
//	
//	//for the graph
//	var row = 0;
//  	for (var idx in ijv_total){
//  		if(x[idx] != 0 ){  	
//  	
//      		solX[row][0] = idx.node_i;
//      		solX[row][1] = idx.node_j;
//      		solX[row][2] = idx.v;
//      		solX[row][3] = x[idx];
//			row ++;
//		}		
//	}	
//}