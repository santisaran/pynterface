DROP TABLE ALIMENTACION;
CREATE TABLE ALIMENTACION
 (
	Tipo			varchar (2), 
	Descripcion			varchar (50)

);
-- CREATE ANY INDEXES ...

DROP TABLE AUTOM_MARCA;
CREATE TABLE AUTOM_MARCA
 (
	CID			int (4), 
	MAKE			varchar (30), 
	LOGOF			varchar

);
-- CREATE ANY INDEXES ...

DROP TABLE AUTOMOTORAS;
CREATE TABLE AUTOMOTORAS
 (
	CID			int (4), 
	RAZON_SOCIAL			varchar (40), 
	DOMICILIO_POSTAL			varchar (80), 
	CIUDAD_POSTAL			varchar (32), 
	PROVINCIA_POSTAL			varchar (40), 
	CP_POSTAL			varchar (20), 
	DOMICILIO_FABRICA			varchar (80), 
	CIUDAD_FABRICA			varchar (32), 
	PROVINCIA_FABRICA			varchar (40), 
	CP_FABRICA			varchar (20), 
	CTO_NOMBRE			varchar (50), 
	CTO_TE1			varchar (28), 
	CTO_TE2			varchar (28), 
	WWW			text, 
	LOGOF			varchar

);
-- CREATE ANY INDEXES ...

DROP TABLE BODYTYPE;
CREATE TABLE BODYTYPE
 (
	Tipo			varchar (2), 
	Descripcion			varchar (40)

);
-- CREATE ANY INDEXES ...

DROP TABLE CONFIG_MODELO;
CREATE TABLE CONFIG_MODELO
 (
	CFGMODELO			varchar (16), 
	DATOS			varchar (100)

);
-- CREATE ANY INDEXES ...

DROP TABLE CUST;
CREATE TABLE CUST
 (
	CID			varchar (16), 
	NAMELAST			varchar (40), 
	NAMEFIRST1			varchar (24), 
	NAMEFIRST2			varchar (24), 
	PHONEHOME			varchar (28), 
	PHONEWORK			varchar (28), 
	BADR1			varchar (80), 
	BADR2			varchar (80), 
	BCITY			varchar (32), 
	BSTATE			varchar (4), 
	BZIP			varchar (20), 
	MADR1			varchar (80), 
	MADR2			varchar (80), 
	MCITY			varchar (32), 
	MSTATE			varchar (4), 
	MZIP			varchar (20), 
	VID1			varchar (16), 
	VID2			varchar (16), 
	VID3			varchar (16), 
	VID4			varchar (16)

);
-- CREATE ANY INDEXES ...

DROP TABLE DRIVETYPE;
CREATE TABLE DRIVETYPE
 (
	Tipo			varchar (2), 
	Descripcion			varchar (40)

);
-- CREATE ANY INDEXES ...

DROP TABLE ENGUNIT;
CREATE TABLE ENGUNIT
 (
	Tipo			varchar (2), 
	Descripcion			varchar (40)

);
-- CREATE ANY INDEXES ...

DROP TABLE ESTACIONES;
CREATE TABLE ESTACIONES
 (
	STATION			varchar (10), 
	DESCRIPCION			varchar (100)

);
-- CREATE ANY INDEXES ...

DROP TABLE FUELTYPE;
CREATE TABLE FUELTYPE
 (
	Tipo			varchar (2), 
	Descripcion			varchar (40)

);
-- CREATE ANY INDEXES ...

DROP TABLE IGNICION;
CREATE TABLE IGNICION
 (
	Tipo			varchar (2), 
	Descripcion			varchar (40)

);
-- CREATE ANY INDEXES ...

DROP TABLE MODELOS;
CREATE TABLE MODELOS
 (
	VID			int (4), 
	CID			int (4), 
	MAKE			varchar (30), 
	MODEL			varchar (40), 
	CYLS			varchar (2), 
	TRANTYPE			varchar (2), 
	FUELTYPE			varchar (2), 
	VEHCLASS			varchar (2), 
	BODYTYPE			varchar (2), 
	DRIVETYPE			varchar (2), 
	ENGSIZE			float (8), 
	ENGUNIT			varchar (2), 
	WEIGHT			float (8), 
	IGNICION			varchar (100), 
	ALIMENTACION			varchar (100), 
	GASES			varchar (100), 
	FOTO			varchar

);
-- CREATE ANY INDEXES ...

DROP TABLE ORDEN_DE_ENSAYO;
CREATE TABLE ORDEN_DE_ENSAYO
 (
	TIPO_SERVICIO			varchar (10), 
	CFGMODELO			varchar (16), 
	TIPO_ENSAYO			varchar (6), 
	NORMA			varchar (12), 
	FECHA_PEDIDO			date (8), 
	FECHA_INICIO			date (8), 
	COMPLETADO			char, 
	OBSERVACIONES			varchar (510), 
	ID_ORDEN			int (4), 
	AFUTURO			char

);
-- CREATE ANY INDEXES ...

DROP TABLE RESULTADO_ENSAYOS;
CREATE TABLE RESULTADO_ENSAYOS
 (
	ID_RESULTADO			int (4), 
	ID_ORDEN			int (4), 
	ID_VEHICULO			int (4), 
	TIPO_SERVICIO			varchar (10), 
	CFGMODELO			varchar (16), 
	TIPO_ENSAYO			varchar (6), 
	NORMA			varchar (12), 
	VIN			varchar (38), 
	DATE			varchar (24), 
	FECHA_INICIO_ENSAYO			date (8), 
	HORA_INICIO_ENSAYO			date (8), 
	OPERADOR			varchar (100), 
	OBSERVACIONES			varchar (510)

);
-- CREATE ANY INDEXES ...

DROP TABLE TAREAS_PROGRAMADAS;
CREATE TABLE TAREAS_PROGRAMADAS
 (
	ID			int (4), 
	ID_ORDEN			int (4), 
	ID_VEHICULO			int (4), 
	FECHA			date (8), 
	HORA			date (8), 
	ETAPA			varchar (100), 
	PRIORIDAD			int (4), 
	ESTADO			varchar (2), 
	OPERADOR			varchar (30), 
	OBSERVACIONES			varchar (510)

);
-- CREATE ANY INDEXES ...

DROP TABLE TEMPORAL;
CREATE TABLE TEMPORAL
 (
	ENSAYO			varchar (20), 
	PROMEDIAR			int (2), 
	TEMP_AMBIENTE			int (2), 
	PRESION			int (2), 
	HUMEDAD			int (2)

);
-- CREATE ANY INDEXES ...

DROP TABLE TESTEOS;
CREATE TABLE TESTEOS
 (
	RECORD			varchar (20), 
	PLATE			varchar (16), 
	MAKE			varchar (30), 
	MODEL			varchar (40), 
	YEAR			varchar (8), 
	ODOMETER			varchar (10), 
	VIN			varchar (34), 
	TESTTYPE			varchar (2), 
	VEH_CLASS			varchar (2), 
	FUEL_TYPE			varchar (2), 
	TRAN_TYPE			varchar (2), 
	CYLINDERS			varchar (4), 
	ENG_SIZE			varchar (8), 
	CURB_WT			varchar (10), 
	TEST_WT			varchar (10), 
	GVWR			varchar (10), 
	LANE_NO			varchar (4), 
	STATION			varchar (10), 
	TEST_DATE			date (8), 
	TIME_BEG1			varchar (12), 
	TIME_END1			varchar (12), 
	S1_LIM_HC			float (8), 
	S1_LIM_CO			float (8), 
	S1_LIM_NO			float (8), 
	S1_LIM_PRG			float (8), 
	S1_HC			float (8), 
	S1_CO			float (8), 
	S1_NO			float (8), 
	S1_CO2			float (8), 
	S1_O2			float (8), 
	S1_SPEED			float (8), 
	S1_LOAD			float (8), 
	S1_PURGE			float (8), 
	S1_RES_HC			varchar (2), 
	S1_RES_CO			varchar (2), 
	S1_RES_NO			varchar (2), 
	S1_RES_PRG			varchar (2), 
	S1_RES_ALL			varchar (2), 
	S2_LIM_HC			float (8), 
	S2_LIM_CO			float (8), 
	S2_LIM_NO			float (8), 
	S2_LIM_PRG			float (8), 
	S2_HC			float (8), 
	S2_CO			float (8), 
	S2_NO			float (8), 
	S2_CO2			float (8), 
	S2_O2			float (8), 
	S2_SPEED			float (8), 
	S2_LOAD			float (8), 
	S2_PURGE			float (8), 
	S2_RES_HC			varchar (2), 
	S2_RES_CO			varchar (2), 
	S2_RES_NO			varchar (2), 
	S2_RES_PRG			varchar (2), 
	S2_RES_ALL			varchar (2), 
	S3_LIM_HC			float (8), 
	S3_LIM_CO			float (8), 
	S3_LIM_NO			float (8), 
	S3_LIM_PRG			float (8), 
	S3_HC			float (8), 
	S3_CO			float (8), 
	S3_NO			float (8), 
	S3_CO2			float (8), 
	S3_O2			float (8), 
	S3_SPEED			float (8), 
	S3_LOAD			float (8), 
	S3_PURGE			float (8), 
	S3_RES_HC			varchar (2), 
	S3_RES_CO			varchar (2), 
	S3_RES_NO			varchar (2), 
	S3_RES_PRG			varchar (2), 
	S3_RES_ALL			varchar (2), 
	PRES_TYPE			float (8), 
	PRES_CAP			varchar (2), 
	TANK_TIME			float (8), 
	TANK_P1			float (8), 
	TANK_P2			float (8), 
	TANK_RATE			float (8), 
	TANK_LIMIT			float (8), 
	TANK_RES			varchar (2), 
	CAP_TIME			float (8), 
	CAP_P1			float (8), 
	CAP_P2			float (8), 
	CAP_RATE			float (8), 
	CAP_LIMIT			float (8), 
	CAP_RES			varchar (2), 
	INSPECTOR			varchar (16), 
	COM_INSP			varchar (8), 
	COM_FLAG			varchar (2), 
	COM_TEXTA			varchar (60), 
	COM_TEXTB			varchar (60), 
	ABRT_INSP			varchar (8), 
	ABRT_TEXT			varchar (60), 
	IM_SECS			float (8), 
	IM_BAD			float (8), 
	IM_VIOL			float (8), 
	IM_EQU			float (8), 
	IM_LOAD			float (8), 
	IM_INERTIA			float (8), 
	IM_SIMIN			float (8), 
	THC			float (8), 
	NOX			float (8), 
	CO			float (8), 
	CO2			float (8), 
	PURGE			float (8), 
	LIM_THC			float (8), 
	LIM_NOX			float (8), 
	LIM_CO			float (8), 
	LIM_PURGE			float (8), 
	RES_THC			varchar (2), 
	RES_NOX			varchar (2), 
	RES_CO			varchar (2), 
	RES_PURGE			varchar (2), 
	RES_TRACE			varchar (2), 
	RES_ALL			varchar (2), 
	C_BACK_THC			float (8), 
	C_BACK_NOX			float (8), 
	C_BACK_CO			float (8), 
	C_BACK_CO2			float (8), 
	C_MPG			float (8), 
	C_DIST			float (8), 
	C_THC			float (8), 
	C_NOX			float (8), 
	C_CO			float (8), 
	C_CO2			float (8), 
	C_PURGE			float (8), 
	C_LIM_THC			float (8), 
	C_LIM_NOX			float (8), 
	C_LIM_CO			float (8), 
	C_LIM_PURG			float (8), 
	REJ_INSP			varchar (4), 
	REJ_EVAP			varchar (4), 
	PF_OVERALL			varchar (2), 
	ENSAYO			varchar (20), 
	PROMEDIAR			int (2), 
	TEMP_AMBIENTE			float (8), 
	PRESION			int (4), 
	HUMEDAD			int (2)

);
-- CREATE ANY INDEXES ...

DROP TABLE TRAT_GASES;
CREATE TABLE TRAT_GASES
 (
	Tipo			varchar (2), 
	Descripcion			varchar (100)

);
-- CREATE ANY INDEXES ...

DROP TABLE VEHIC_RECEPCION;
CREATE TABLE VEHIC_RECEPCION
 (
	ID_VEHICULO			int (4), 
	ID_ORDEN			int (4), 
	VIN			varchar (38), 
	VID			int (4), 
	MOTOR			varchar (36), 
	CHASIS			varchar (34), 
	PLATE			varchar (16), 
	STATE			varchar (4), 
	YEAR			float (8), 
	MAKE			varchar (30), 
	MODEL			varchar (40), 
	CONVENIO			varchar (100), 
	CID			varchar (100), 
	ODOMETER			float (8), 
	KM_FINAL			int (4), 
	FECHA_RECEPCION			date (8), 
	HORA_RECEPCION			date (8), 
	RECIBIDO_POR			varchar (100), 
	INGRESA			char, 
	CONDUCTOR_IN			varchar (50), 
	REMITO			varchar (100), 
	FECHA_ENTREGA			date (8), 
	HORA_ENTREGA			date (8), 
	ENTREGADO_POR			varchar (100), 
	CONDUCTOR_OUT			varchar (100), 
	AUTORIZACION			varchar (100), 
	NOTES1			varchar (510), 
	NOTES2			varchar (510)

);
-- CREATE ANY INDEXES ...

DROP TABLE VEHIC_TECNICOS_ENSAYO;
CREATE TABLE VEHIC_TECNICOS_ENSAYO
 (
	ID			int (4), 
	ID_ORDEN			int (4), 
	ID_VEHICULO			int (4), 
	VIN			varchar (34), 
	FECHA_REVISION			date (8), 
	HORA_REVISON			date (8), 
	TEMPERATURA			int (2), 
	HUMEDAD			varchar (34), 
	PRESION			int (4), 
	VOL_COMB			float (8), 
	COMP_COMB			varchar (30), 
	TRACCION			varchar (40), 
	4X4_DELANTERA			char, 
	NEUMATICOS			varchar (100), 
	PRESION_NEUM			int (4), 
	ACCESORIOS			char, 
	ESCAPE			char, 
	CATALIZADOR			char, 
	TEMP_AGUA_A			float (8), 
	TEMP_ACEITE_A			float (8), 
	PREACOND_T			date (8), 
	RPM			float (8), 
	TEMP_AGUA_P			float (8), 
	TEMP_ACEITE_P			int (2), 
	T_TRANSC			date (8), 
	REVISADO_POR			varchar (100), 
	SUPERVISADO_POR			varchar (100), 
	OBS_TECNICAS			varchar (200), 
	ENSAYO			varchar (100), 
	FECHA_ENSAYO			date (8), 
	CONDUCTOR			varchar (100), 
	ANALISTA			varchar (100), 
	RESPONSABLE			varchar (100), 
	OBS_ENSAYO			varchar (100)

);
-- CREATE ANY INDEXES ...

DROP TABLE VEHICLASS;
CREATE TABLE VEHICLASS
 (
	Tipo			varchar (2), 
	Descripcion			varchar (40)

);
-- CREATE ANY INDEXES ...

DROP TABLE VEHICLE;
CREATE TABLE VEHICLE
 (
	VID			varchar (16), 
	CID			varchar (16), 
	VIN			varchar (34), 
	PLATE			varchar (16), 
	STATE			varchar (4), 
	YEAR			float (8), 
	MAKE			varchar (30), 
	MODEL			varchar (40), 
	CYLS			varchar (2), 
	TRANTYPE			varchar (2), 
	FUELTYPE			varchar (2), 
	VEHCLASS			varchar (2), 
	BODYTYPE			varchar (2), 
	DRIVETYPE			varchar (2), 
	ENGSIZE			float (8), 
	ENGUNIT			varchar (2), 
	WEIGHT			float (8), 
	ODOMETER			float (8), 
	NOTES1			varchar (80), 
	NOTES2			varchar (80)

);
-- CREATE ANY INDEXES ...

DROP TABLE CILINDROS;
CREATE TABLE CILINDROS
 (
	Tipo			varchar (2), 
	Descripcion			varchar (40)

);
-- CREATE ANY INDEXES ...

DROP TABLE RESULTADOS;
CREATE TABLE RESULTADOS
 (
	RECORD			varchar (20), 
	SECOND			float (8), 
	SPEED			float (8), 
	THC			float (8), 
	NOX			float (8), 
	CO			float (8), 
	CO2			float (8), 
	O2			float (8), 
	PURGE			float (8), 
	DISTANCE			float (8), 
	VMIX			float (8)

);
-- CREATE ANY INDEXES ...

DROP TABLE TRANSTYPE;
CREATE TABLE TRANSTYPE
 (
	Tipo			varchar (2), 
	Descripcion			varchar (40)

);
-- CREATE ANY INDEXES ...



-- CREATE ANY Relationships ...

-- relationships are not supported for mysql
