/* ************** LDR ************** */
int get_LDR() {
  int LDR_meting = analogRead(LDR);
  int lichtpercentage = (1023 - LDR_meting) / 4;
  return lichtpercentage;
}
