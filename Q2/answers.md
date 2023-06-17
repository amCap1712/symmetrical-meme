### a.
#### How many types of tigers can be found in the taxonomy table of the dataset? 
There are **8** tigers in the taxonomy table of the dataset.
```sql
select count(*) from taxonomy where species like 'Panthera tigris%';
```
####  What is the "ncbi_id" of the Sumatran Tiger? (hint: use the biological name of the tiger)
The ncbi_id of the Sumatran Tiger is **9695**.

```sql
select ncbi_id, species from taxonomy where species like 'Panthera tigris sumatrae%';
```

### b.
#### Find all the columns that can be used to connect the tables in the given database.
There are 6 main tables listed in the Rfam docs: `rfamseq`, `taxonomy`, `family`, `clan_membership`, `clan` and `full_region`.
For these tables, here is a list of columns that tables can be connected using. These have identified using the existing
FOREIGN KEYs on the tables.

| Table 1  | Table 2         | Foreign Key Column |
|----------|-----------------|--------------------|
| taxonomy | rfamseq         | ncbi_id            |
| family   | full_region     | rfam_acc           |
| taxonomy | full_region     | rfamseq_acc        |
| clan     | clan_membership | clan_acc           |
| family   | clan_membership | rfam_acc           |
| family   | wikitext        | auto_wiki          |

### c.
#### Which type of rice has the longest DNA sequence? (hint: use the rfamseq and the taxonomy tables) 

`Oryza sativa Indica Group` is the rice species with the longest DNA sequence.

`Oryza sativa` and `Oryza rufipogon` are the two base rice species. To include the variants we use `LIKE` operator
and to exclude the viruses which share the similar species name we add a condition that the species is a Eukaryote.

```sql
select *
  from taxonomy
  join rfamseq
 using (ncbi_id)
 where (species like 'Oryza sativa%' or species like 'Oryza rufipogon%')
   and tax_string like 'Eukaryota;%'
order by length desc
limit 1;
```

### d.
#### We want to paginate a list of the family names and their longest DNA sequence lengths (in descending order of length) where only families that have DNA sequence lengths greater than 1,000,000 are included. Give a query that will return the 9th page when there are 15 results per page. (hint: we need the family accession ID, family name and the maximum length in the results)

```sql
select rfam_acc
     , rfamseq_acc
     , r.length
  from family f
  join full_region fr
 using (rfam_acc)
  join rfamseq r
 using (rfamseq_acc)
 where r.length >= 1000000
order by r.length DESC
LIMIT 15
OFFSET 120
```
